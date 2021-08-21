#ifndef MY_PATH_UTIL
#define MY_PATH_UTIL


#include <string>
#include <iostream>
#include <sstream>

#include <utility>
#include <vector>
#include <functional>

#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <cstdio>

#include "myStringUtil.h"

namespace sh {
	namespace path {
		enum file_type // from boost
		{ 
			status_unknown,
			file_not_found,
			regular_file,
			directory_file,
			// the following will never be reported by some operating or file systems
			symlink_file,
			block_file,
			character_file,
			fifo_file,
			socket_file,
			type_unknown // file does exist, but isn't one of the above types
		};
	
	
		class Path {
		private:
			std::string _str_path;
			// file_type _type;
			
			
			operator std::string() const {
				return _str_path;
			}
			
		public:
			Path() : _str_path() {};
			
			Path(const std::string & __str_path) : _str_path(__str_path) {};
			// Path(const char * __c_str_path) : _str_path(__c_str_path) {};
			
			Path(const Path & path) : _str_path(path) {};
			
			Path & operator=(const Path & path) {
				_str_path = path;
				return *this;
			}
			
			file_type type() const {
				struct stat stat_buf;
				
				if (lstat(_str_path.c_str(), &stat_buf) < 0) {
					return file_not_found;
				}
				
				file_type __type = status_unknown;
				if ( S_ISREG(stat_buf.st_mode) ) {
					__type = regular_file; 
				} else if ( S_ISDIR(stat_buf.st_mode) ) {
					__type = directory_file;
				} else if ( S_ISCHR(stat_buf.st_mode) ) {
					__type = character_file;
				} else if ( S_ISBLK(stat_buf.st_mode) ) {
					__type = block_file;
				} else if ( S_ISFIFO(stat_buf.st_mode) ) {
					__type = fifo_file;
				} else if ( S_ISLNK(stat_buf.st_mode) ) {
					__type = symlink_file;
				} else if ( S_ISSOCK(stat_buf.st_mode) ) {
					__type = socket_file;
				} else {
					__type = type_unknown;
				}
				return __type;
			}
			
			bool isExist() {
				if (type() != file_not_found) {
					return true;
				}
				return false;
			}
			/*
			Path & operator=(const std::string & path) {
				_str_path = path;
				return *this;
			}
			*/
			
			const std::string & str() const {
				return _str_path;
			}
			
			Path basename() const;
			Path dirname() const;
			std::string suffix() const;
			
			// friend std::ostream & operator<<(std::ostream & os, const Path & obj);
			friend Path operator+(const Path & p1, const Path & p2);
		};
		
		std::ostream & operator<<(std::ostream & os, const Path & obj);
		
		/*
		inline int rename(const Path & oldname, const Path & newname) {
			return std::rename(oldname.str().c_str(), newname.str().c_str());
		};
		*/
		int rename(const Path & oldname, const Path & newname);
		int remove(const Path & path);
		int remove_all(const Path & path);
		
		template <typename Func>
		int traverse(const Path & path, Func f) {
			file_type type = path.type();
			if (type == regular_file || type == symlink_file) {
				return f(path);
			} else if (type == directory_file) {
				DIR * dir = opendir(path.str().c_str());
				if (dir == NULL) {
					std::cerr << "Error: can't open dir: " << path << std::endl;
					return -1;
				}
				
				int result(0);
				struct dirent * dirp = NULL;
				while ((dirp = readdir(dir)) != NULL) {
					Path name(dirp->d_name);
					if (name.str() == "." || name.str() == "..") {
						continue;
					}
					Path tmp_path = path + name;
					if ( traverse(tmp_path, f) < 0 ) {
						result = -1;
					}
				}
				closedir(dir);
				if (f(path) < 0) {
					result = -1;
				}
				return result;
			} else {
				return -1;
			}
		}
	}
}


#endif // MY_PATH_UTIL
