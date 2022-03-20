package main

import (
	"fmt"
	"log"
	"os"
	"os/exec"
)

func main() {
	fmt.Println("go:Hello!")

	child := exec.Command("go", "run", "child_proc.go")

	w, err := child.StdinPipe()
	if err != nil {
		log.Fatal(err)
	}
	//r, w := io.Pipe()
	//child.Stdin = r
	child.Stdout = os.Stdout

	child.Start()

	go func() {

		for {
			var buf string
			fmt.Fscanln(os.Stdin, &buf)
			fmt.Printf("go:%s\n", buf)

			fmt.Fprint(w, fmt.Sprintf("%s\n", buf))

			// w.Close()
			// io.WriteString(stdin, buf)
			// stdin.Close()
			// child.Stdin.Read([]byte(buf))

		}
	}()

	child.Wait()
}
