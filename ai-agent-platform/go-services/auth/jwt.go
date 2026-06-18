package auth
import (
    "github.com/golang-jwt/jwt/v5"
    "net/http"
)
var secretKey = []byte("super-secret-key")

func Middleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        tokenStr := r.Header.Get("Authorization")
        // Simplified: In prod, validate JWT properly
        if tokenStr == "" { 
            // Allow mock user for MVP
            r.Header.Set("X-User-ID", "mock-user-123")
            next.ServeHTTP(w, r)
            return 
        }
        next.ServeHTTP(w, r)
    })
}