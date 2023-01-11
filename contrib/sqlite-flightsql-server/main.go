package main

import (
	"log"
	"net"
	"os"

	"github.com/apache/arrow/go/v11/arrow/flight"
	"github.com/apache/arrow/go/v11/arrow/flight/flightsql"
	"github.com/apache/arrow/go/v11/arrow/flight/flightsql/example"
	"github.com/apache/arrow/go/v11/arrow/memory"
	"google.golang.org/grpc"
)

func main() {
	addr := os.Getenv("ADDR")
	if addr == "" {
		addr = ":3000"
	}
	lis, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatalf("failed to listen: %v", err)
	}

	server := grpc.NewServer()
	sqliteServer, err := example.NewSQLiteFlightSQLServer()
	if err != nil {
		log.Fatalf("flight sql server: %v", err)
	}
	sqliteServer.Alloc = memory.NewCheckedAllocator(memory.DefaultAllocator)

	flight.RegisterFlightServiceServer(server, flightsql.NewFlightServer(sqliteServer))

	for svc, info := range server.GetServiceInfo() {
		for _, method := range info.Methods {
			log.Printf("%s/%s\n", svc, method.Name)
		}
	}
	log.Println("listening:", addr)
	server.Serve(lis)
}
