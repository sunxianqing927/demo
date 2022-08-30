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

/// GET����
string GetRequest(char* host, char* path);
string GetRequest(string url);

/// POST����
string PostRequest(char* host, char* path, string form);
