package main

import (
    "encoding/json"
    "log"
    "net/http"
    "google.golang.org/grpc"
    "google.golang.org/grpc/credentials/insecure"
    pb "ai-agent-platform/proto" // Adjust import path
)

func main() {
    // Connect to Orchestrator via gRPC
    conn, err := grpc.Dial("localhost:50051", grpc.WithTransportCredentials(insecure.NewCredentials()))
    if err != nil { log.Fatal(err) }
    client := pb.NewOrchestratorServiceClient(conn)

    http.HandleFunc("/api/tasks", func(w http.ResponseWriter, r *http.Request) {
        if r.Method != "POST" { http.Error(w, "Method not allowed", 405); return }
        
        var req struct { Prompt string `json:"prompt"` }
        json.NewDecoder(r.Body).Decode(&req)

        // Call Orchestrator via gRPC
        resp, err := client.CreateTask(r.Context(), &pb.CreateTaskRequest{
            UserId: "mock-user-123", Prompt: req.Prompt,
        })
        if err != nil { http.Error(w, err.Error(), 500); return }

        json.NewEncoder(w).Encode(map[string]string{"task_id": resp.TaskId, "status": resp.Status})
    })

    log.Println("Gateway running on :8080")
    http.ListenAndServe(":8080", nil)
}