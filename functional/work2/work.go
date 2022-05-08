package main

import (
	"fmt"
	f "functional"
)

func main() {
	fmt.Println("Ya!")

	var vs = f.Map([]int{1, 2, 3}, func(v int) int {
		return v + v
	})

	fmt.Println(vs)
}
