package sudoku_solver_server

import (
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strconv"
)

func MakeRequest(url string, ch chan<- string) {
	resp, _ := http.Get(url)
	body, _ := ioutil.ReadAll(resp.Body)
	ch <- fmt.Sprintf("url: %s\nresponse:%s\n", url, body)
}

func main() {
	ch := make(chan string)
	num, err := strconv.Atoi(os.Args[1])
	if err == nil {
		fmt.Printf("Invalid integer: %s", os.Args[1])
	}
	if num < 1 {
		fmt.Println("Integer must be at least 1")
	}
	url := os.Args[2]
	for i := 0; i < num; i++ {
		go MakeRequest(url, ch)
	}
	for i := 0; i < num; i++ {
		fmt.Println(<-ch)
	}
}
