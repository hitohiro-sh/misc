package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println("go:child:Hello!")
	for {
		var buf string
		fmt.Fscanln(os.Stdin, &buf)
		fmt.Printf("go:child:%s\n", buf)
	}
}
