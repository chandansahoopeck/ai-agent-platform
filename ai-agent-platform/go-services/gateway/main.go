package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"strings"

	"github.com/jackc/pgx/v5/pgxpool"
	"google.golang.org/grpc"
	"google.golang.org/grpc/credentials/insecure"
	pb "ai-agent-platform/proto"
)

var db *pgxpool.Pool

// CORS Middleware
func corsMiddleware(next http.HandlerFunc) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		w.Header().Set("Access-Control-Allow-Origin", "*")
		w.Header().Set("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
		w.Header().Set("Access-Control-Allow-Headers", "Content-Type")
		
		if r.Method == "OPTIONS" {
			w.WriteHeader(http.StatusOK)
			return
		}
		
		next(w, r)
	}
}

func main() {
	var err error
	db, err = pgxpool.New(context.Background(), "postgres://admin:password@localhost:5432/agents_db")
	if err != nil {
		log.Fatal("Failed to connect to database:", err)
	}
	defer db.Close()

	conn, err := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
	if err != nil {
		log.Fatal("Failed to connect to orchestrator:", err)
	}
	client := pb.NewOrchestratorServiceClient(conn)

	// POST /api/tasks
	http.HandleFunc("/api/tasks", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "POST" {
			http.Error(w, "Method not allowed", 405)
			return
		}
		var req struct {
			Prompt string `json:"prompt"`
		}
		json.NewDecoder(r.Body).Decode(&req)

		resp, err := client.CreateTask(r.Context(), &pb.CreateTaskRequest{
			UserId: "mock-user-123",
			Prompt: req.Prompt,
		})
		if err != nil {
			http.Error(w, err.Error(), 500)
			return
		}

		json.NewEncoder(w).Encode(map[string]string{
			"task_id": resp.TaskId,
			"status":  resp.Status,
		})
	}))

	// GET /api/tasks/{id}
	http.HandleFunc("/api/tasks/", corsMiddleware(func(w http.ResponseWriter, r *http.Request) {
		if r.Method != "GET" {
			http.Error(w, "Method not allowed", 405)
			return
		}

		taskID := strings.TrimPrefix(r.URL.Path, "/api/tasks/")
		if taskID == "" {
			http.Error(w, "Task ID required", 400)
			return
		}

		var status string
		var result string

		err := db.QueryRow(context.Background(),
			"SELECT status FROM tasks WHERE id = $1", taskID).Scan(&status)
		if err != nil {
			log.Printf("Database error fetching task %s: %v", taskID, err)
			http.Error(w, "Task not found", 404)
			return
		}

		if status == "COMPLETED" {
			err := db.QueryRow(context.Background(),
				"SELECT data FROM results WHERE execution_id = $1", taskID).Scan(&result)
			if err != nil {
				log.Printf("Database error fetching result for task %s: %v", taskID, err)
			}
		}

		json.NewEncoder(w).Encode(map[string]string{
			"task_id": taskID,
			"status":  status,
			"result":  result,
		})
	}))

	log.Println("Gateway running on :8080 with CORS enabled")
	http.ListenAndServe(":8080", nil)
}