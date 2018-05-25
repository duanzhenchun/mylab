package main

import (
	"fmt"
	"math"
)

func MultiTrunc(val float64, multi float64, prec int) float64 {
	precPow10 := math.Pow10(prec)
	return math.Trunc(val*multi*precPow10+0.5) / precPow10
}

func main() {
	println(MultiTrunc(1.2, 1.0, 2))
	fmt.Printf("%.1f\n", 1.23)
}
