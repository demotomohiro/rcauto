#include <iostream>
#include <fstream>
#include <thread>

using namespace std;

int main(int argc, char* argv[]) {
    if(argc > 1) {
        cout << "Got arguments: ";
        for(int i = 0; i < argc; ++i) {
            cout << "'" << argv[i] << "' ";
        }
        cout << '\n';
    }

    cout << "Starting test cpp" << endl;
    {
        ofstream o("test000.png");
        o << "test000 image" << endl;
    }
    {
        ofstream o("log");
        o << "test log" << endl;
    }
    cerr << "Error test" << endl;
    std::this_thread::sleep_for(std::chrono::seconds(6));
    cout << "finished" << endl;
}
