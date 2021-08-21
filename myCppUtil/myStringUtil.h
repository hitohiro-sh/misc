#ifndef MY_STRING_UTIL
#define MY_STRING_UTIL


#include <string>
#include <iostream>
#include <sstream>

#include <vector>
#include <functional>

namespace sh {



	// New
	// void split(std::vector<std::string> & strs, const std::string & str, unaryPredicate is);
	void split(std::vector<std::string> & strs, const std::string & str);
	void split(std::vector<std::string> & strs, const std::string & str, const char c);
	
	
	template<typename UnaryPredicate>
	void split(std::vector<std::string> & strs, const std::string & str, UnaryPredicate is) {
		int len = 0;
		int start = 0;
		for (unsigned int i = 0; i < str.size(); i++) {
				
			if (is(str[i])) {
				if (len > 0) {
					strs.push_back(str.substr(start, len));
				}
				start = i + 1;
				len = 0;
			} else {
				len++;	
			}
		}
		if (len > 0) {
			strs.push_back(str.substr(start, len));
		}
	}
	
	
	// std::string join(const std::vector<std::string> & strs);
	// std::string join(const std::vector<std::string> & strs, const char c);
	// std::string join(const std::vector<std::string> & strs, const std::string & str);
	template <typename List, typename T>
	std::string join(const List & list, const T & t) {
		if (list.empty()) {
			return "";
		}
		// std::string buf("");
		std::ostringstream oss;
		
		
		oss << list.front();
		for (typename List::const_iterator it = list.begin() + 1; it != list.end(); it++) {
			oss << t << *it;
		}
		
		return oss.str();
	}
	
	template <typename List>
	std::string join(const List & list) {
		return join(list, ' ');
	}
	
	template <typename UnaryPredicate>
	std::string lstrip(const std::string & str, UnaryPredicate is) {
		for (unsigned int i = 0; i < str.size(); i++) {
			if (! is(str[i])) {
				return str.substr(i, str.size() - i);
			}
		}
		return "";
	}
	
	template <typename UnaryPredicate>
	std::string rstrip(const std::string & str, UnaryPredicate is) {
		if (str.size() == 0) {
			return "";
		}
		
		for (unsigned int i = str.size() - 1; i >= 1; i--) {
			if (! is(str[i])) {
				return str.substr(0, i + 1);
			}
		}
		return "";
	}
	
	
	template <typename UnaryPredicate>
	std::string strip(const std::string & str, UnaryPredicate is) {
		unsigned int i(0);
		unsigned int start(0), end(0);

		for (i = 0; i < str.size(); i++) {
			if (! is(str[i])) {
				start = i;
				break;
			}
		}
		
		if (i == str.size()) {
			return "";
		}
		
		for (i = str.size() - 1; i >= 0; i--) {
			if (! is(str[i])) {
				end = i;
				break;
				// return str.substr(0, i + 1);
			}
		}
		
		if (i < 0) {
			return "";
		}
		
		return str.substr(start, end - start + 1);
	}
	
	
	std::string lstrip(const std::string & str);
	std::string lstrip(const std::string & str, const char c);
	std::string rstrip(const std::string & str);
	std::string rstrip(const std::string & str, const char c);
	std::string strip(const std::string & str);
	std::string strip(const std::string & str, const char c);
	
}

#endif // MY_STRING_UTIL
