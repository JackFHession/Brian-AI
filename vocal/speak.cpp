#include <iostream>
#include <cstdlib>

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: ./speak <text_to_speak>" << std::endl;
        return 1;
    }
    
    std::string command = "espeak \"";
    for (int i = 1; i < argc; ++i) {
        command += argv[i];
        if (i < argc - 1) {
            command += " ";
        }
    }
    command += "\"";
    
    int result = std::system(command.c_str());
    if (result != 0) {
        std::cerr << "Error executing espeak" << std::endl;
        return 1;
    }
    
    return 0;
}
