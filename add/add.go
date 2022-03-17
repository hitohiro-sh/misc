package main

import (
	"fmt"

	c "golang.org/x/exp/constraints"
	s "golang.org/x/exp/slices"
)

func Add[T c.Integer](x, y T) T {
	return x + y
}

func main() {
	x := 1
	y := 2
	fmt.Printf("%v + %v = %v\n", x, y, Add(x, y))

	datas := []int{1, 2, 3}
	datas = s.Insert(datas, 3, 4)
	fmt.Printf("%v\n", datas)
}
