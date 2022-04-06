package functional

func Map[T any, U any](arr []T, f func(v T) U) []U {
	ret := []U{}
	for _, v := range arr {
		ret = append(ret, f(v))
	}
	return ret
}

func Reduce[T any, U any](init U, arr []T, f func(v T, acc U) U) (ret U) {
	ret = init
	for _, v := range arr {
		ret = f(v, ret)
	}
	return
}
