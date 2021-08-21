


#include "myPathUtil.h"
#include "myStringUtil.h"

#include <string>

namespace sh {
	namespace path {
		typedef std::string::size_type size_type;
	
		Path Path::basename() const {
			size_type pos = this->_str_path.rfind("/");
				// Path basename;
			if (pos == std::string::npos) {
				return Path(*this);
					// basename = *this;
			} else {
				return Path(this->_str_path.substr(pos + 1));
					// basename = this->_str_path.substr(pos + 1);
			}
				// return basename;
		}
			
		Path Path::dirname() const {
			size_type pos = this->_str_path.rfind("/");
				
			if (pos == std::string::npos) {
				return Path("");
			} else {
				return Path(this->_str_path.substr(0, pos));
			}
		}
			
		std::string Path::suffix() const {
			// throw 1;
			// return "";
			size_type pos = this->_str_path.rfind(".");
			
			std::string suffix_str("");
			if (pos != std::string::npos) {
				suffix_str = this->_str_path.substr(pos + 1);
			}
			return suffix_str;
		}
			
			
		std::ostream & operator<<(std::ostream & os, const Path & obj) {
			os << obj.str();
			return os;
		}
		
		
		Path operator+(const Path & p1, const Path & p2) {
			if (p1.str() != "") {
				Path new_path(rstrip(p1, '/') + "/" + lstrip(p2, '/'));
				return new_path;
			} else {
				return Path(p2);
			}
		}
		
		int rename(const Path & oldname, const Path & newname) {
			return std::rename(oldname.str().c_str(), newname.str().c_str());
		}
		
		int remove(const Path & path) {
			return std::remove(path.str().c_str());
		}
		
		
		
		int remove_all(const Path & path) {
			return traverse(path, sh::path::remove);
		}
		/*
		int remove_all(const Path & path) {
			file_type type = path.type();
			if (type == regular_file || type == symlink_file) {
				return remove(path);
			} else if (type == directory_file) {
				DIR * dir = opendir(path.str().c_str());
				if (dir == NULL) {
					std::cerr << "Error: can't open dir: " << path << std::endl;
					return -1;
				}
				
				int result = 0;
				struct dirent * dirp = NULL;
				while ((dirp = readdir(dir)) != NULL) {
					Path name(dirp->d_name);
					if (name.str() == "." || name.str() == "..") {
						continue;
					}
					Path tmp_path = path + name;
					if ( remove_all(tmp_path) < 0 ) {
						result = -1;
					}
				}
				closedir(dir);
				if (remove(path) < 0) {
					result = -1;
				}
				return result;
			} else {
				return -1;
			}
		}
		*/
		
	}
}
