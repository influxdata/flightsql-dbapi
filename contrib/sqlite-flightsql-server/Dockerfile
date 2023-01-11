FROM golang:1.19-alpine as build
WORKDIR /go/src/app
COPY . .
RUN go mod download
RUN CGO_ENABLED=0 go build -o /go/bin/app

FROM gcr.io/distroless/static-debian11
COPY --from=build /go/bin/app /
EXPOSE 3000
USER nonroot:nonroot
CMD ["/app"]
