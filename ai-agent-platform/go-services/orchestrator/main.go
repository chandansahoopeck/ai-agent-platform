package main

import (
    "context"
    "log"
    "net"
    "github.com/google/uuid"
    "github.com/jackc/pgx/v5/pgxpool"
    "github.com/nats-io/nats.go"
    "google.golang.org/grpc"
    pb "ai-agent-platform/proto"
)

type Server struct {
    pb.UnimplementedOrchestratorServiceServer
    db   *pgxpool.Pool
    nats *nats.Conn
}

func (s *Server) CreateTask(ctx context.Context, req *pb.CreateTaskRequest) (*pb.CreateTaskResponse, error) {
    taskID := uuid.New().String()
    
    // 1. Save to Postgres
    s.db.Exec(ctx, "INSERT INTO tasks (id, user_id, status) VALUES ($1, $2, 'PENDING')", taskID, req.UserId)

    // 2. Publish to Pub/Sub (NATS)
    s.nats.Publish("task.created", []byte(taskID))

    return &pb.CreateTaskResponse{TaskId: taskID, Status: "PENDING"}, nil
}

func main() {
    db, _ := pgxpool.New(context.Background(), "postgres://admin:password@localhost:5432/agents_db")
    nc, _ := nats.Connect("nats://localhost:4222")
    
    srv := &Server{db: db, nats: nc}
    lis, _ := net.Listen("tcp", ":50051")
    grpcServer := grpc.NewServer()
    pb.RegisterOrchestratorServiceServer(grpcServer, srv)
    
    log.Println("Orchestrator gRPC running on :50051")
    grpcServer.Serve(lis)
}