package main

import (
	"encoding/json"
	"fmt"
	"io"
	"log"
	"os"
)

type Api struct {
	apiMap map[string]func(data string)
	reader io.Reader
}

func ApiNew(reader io.Reader) *Api {
	return &Api{
		apiMap: map[string]func(arg string){},
		reader: reader,
	}
}

func (api *Api) On(id string, callback func(arg string)) {
	api.apiMap[id] = callback
}

func (api *Api) Run() {
	apicall := func(m, v string) {
		if f, ok := api.apiMap[m]; ok {
			f(v)
		}
	}

	for {
		var buf string
		fmt.Fscanln(api.reader, &buf)
		// fmt.Printf("go:child:%s\n", buf)
		// break
		var inst []string
		err := json.Unmarshal([]byte(buf), &inst)
		if err != nil {
			log.Fatal(err)
		}
		apicall(inst[0], inst[1])

	}
}

func main() {
	fmt.Println("go:child:Hello!")

	api := ApiNew(os.Stdin)
	api.On("f1", func(data string) {
		fmt.Printf("go:child:f1:%s\n", data)
	})
	api.On("f2", func(data string) {
		fmt.Printf("go:child:f2:%s\n", data)
	})

	api.Run()

	//api := map[string]func(data string){
	//	"f1": func(data string) {
	//		fmt.Printf("go:child:f1:%s\n", data)
	//	},
	//	"f2": func(data string) {
	//		fmt.Printf("go:child:f2:%s\n", data)
	//	}}

	//apicall := func(m, v string) {
	//	if f, ok := api[m]; ok {
	//		f(v)
	//	}
	//}

	//for {
	//	var buf string
	//	fmt.Fscanln(os.Stdin, &buf)
	//	fmt.Printf("go:child:%s\n", buf)
	//	// break
	//	var inst []string
	//	err := json.Unmarshal([]byte(buf), &inst)
	//	if err != nil {
	//		log.Fatal(err)
	//	}
	//	apicall(inst[0], inst[1])
	//
	//	}
}
