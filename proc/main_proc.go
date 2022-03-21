package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
	"os/exec"
	"strings"
)

type ApiClient struct {
	child  *exec.Cmd
	writer io.Writer
}

func ApiClientNew(child *exec.Cmd) *ApiClient {
	return &ApiClient{
		child: child,
	}
}

func (client *ApiClient) Start() {
	writer, err := client.child.StdinPipe()
	if err != nil {
		log.Fatal(err)
	}
	client.writer = writer

	client.child.Start()
}

func (client *ApiClient) Wait() {
	client.child.Wait()
}

func (client *ApiClient) Send(id, data string) error {
	writer := client.writer
	obj, err := json.Marshal([]string{id, data})
	if err == nil {
		fmt.Fprint(writer, fmt.Sprintf("%s\n", obj))
		return nil
	} else {
		return err
	}
}

func (client *ApiClient) StdoutPipe() (io.ReadCloser, error) {
	return client.child.StdoutPipe()
}

func main() {

	fmt.Println("go:Hello!")

	// child := exec.Command("go", "run", "child_proc.go")

	client := ApiClientNew(exec.Command("go", "run", "child_proc.go"))

	//w, err := child.StdinPipe()
	//if err != nil {
	//	log.Fatal(err)
	//}
	//r, w := io.Pipe()
	//child.Stdin = r
	//child.Stdout = os.Stdout
	r, err := client.StdoutPipe()
	if err != nil {
		log.Fatal(err)
	}

	client.Start()

	go func() {
		for {
			var buf string
			fmt.Fscanln(r, &buf)
			fmt.Printf("go:out:%s\n", buf)
		}
	}()

	go func() {

		for {
			var buf string
			fmt.Fscanln(os.Stdin, &buf)
			fmt.Printf("go:in:%s\n", buf)

			inst := strings.Split(buf, ":")

			client.Send(inst[0], inst[1])
			//obj, err := json.Marshal(inst)
			//if err == nil {
			//	fmt.Printf("%s\n", obj)
			//	fmt.Fprint(w, fmt.Sprintf("%s\n", obj))
			//}

		}
	}()

	client.Wait()
}
