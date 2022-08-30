//
//  NetworkRequest.h
//
//  Created by duzixi.com on 15/8/25.
//

#include <stdio.h>
#include <iostream>
#include <fstream>
#include<boost/json.hpp>
#include <boost/asio.hpp>

using namespace std;

/// GET«Î«Û
string GetRequest(char* host, char* path);
string GetRequest(string url);

/// POST«Î«Û
string PostRequest(char* host, char* path, string form);
