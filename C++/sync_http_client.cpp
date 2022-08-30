//
// sync_client.cpp
// ~~~~~~~~~~~~~~~
//
// Copyright (c) 2003-2022 Christopher M. Kohlhoff (chris at kohlhoff dot com)
//
// Distributed under the Boost Software License, Version 1.0. (See accompanying
// file LICENSE_1_0.txt or copy at http://www.boost.org/LICENSE_1_0.txt)
//

#include <iostream>
#include <istream>
#include <ostream>
#include <string>
#include <boost/asio.hpp>
#include<boost/json.hpp>

using boost::asio::ip::tcp;

std::string testdata()
{
    boost::json::value jv = {
    { "keyWord", "18"},
    { "limitCount", 5 },
    };
    return boost::json::serialize(jv);
}
//sync_http_client_main
int main(int argc, const char* argv[])
{
    SetConsoleOutputCP(CP_UTF8);
    try
    {
        //if (argc != 3)
        //{
        //    std::cout << "Usage: sync_client <server> <path>\n";
        //    std::cout << "Example:\n";
        //    std::cout << "  sync_client www.boost.org /LICENSE_1_0.txt\n";
        //    return 1;
        //}

        boost::asio::io_context io_context;

        // Get a list of endpoints corresponding to the server name.
        //tcp::resolver resolver(io_context);
        //tcp::resolver::results_type endpoints = resolver.resolve(argv[1], "http");

        // Try each endpoint until we successfully establish a connection.
        tcp::socket socket(io_context);
       // boost::asio::connect(socket, endpoints);
        socket.connect(tcp::endpoint(boost::asio::ip::address_v4::from_string("127.0.0.1"), 22222));

        // Form the request. We specify the "Connection: close" header so that the
        // server will close the socket after transmitting the response. This will
        // allow us to treat all data up until the EOF as the content.
        auto form = testdata();
        boost::asio::streambuf request;
        std::ostream request_stream(&request);
        request_stream << "POST " <<"/qm/query/trade" << " HTTP/1.1\r\n";
       // request_stream << "Host: " << "127.0.0.1:22222" << "\r\n";
        request_stream << "Accept: */*\r\n";
        request_stream << "Content-Type:application/json\r\n";
        request_stream << "Content-Length: " << form.length() << "\r\n";
        request_stream << "Connection: close\r\n\r\n";
        request_stream << form; //POST 发送的数据本身不包含多于空行
        // Send the request.
        boost::asio::write(socket, request);

        // Read the response status line. The response streambuf will automatically
        // grow to accommodate the entire line. The growth may be limited by passing
        // a maximum size to the streambuf constructor.
        boost::asio::streambuf response;
        boost::asio::read_until(socket, response, "\r\n");

        // Check that response is OK.
        std::istream response_stream(&response);
        std::string http_version;
        response_stream >> http_version;
        unsigned int status_code;
        response_stream >> status_code;
        std::string status_message;
        std::getline(response_stream, status_message);
        if (!response_stream || http_version.substr(0, 5) != "HTTP/")
        {
            std::cout << "Invalid response\n";
            return 1;
        }
        if (status_code != 200)
        {
            std::cout << "Response returned with status code " << status_code << "\n";
            return 1;
        }

        // Read the response headers, which are terminated by a blank line.
        boost::asio::read_until(socket, response, "\r\n\r\n");

        // Process the response headers.
        std::string header;
        while (std::getline(response_stream, header) && header != "\r")
            std::cout << header << "\n";
        std::cout << "\n";

        // Write whatever content we already have to output.
        if (response.size() > 0)
            std::cout << &response;

        // Read until EOF, writing data to output as we go.
        boost::system::error_code error;
        while (boost::asio::read(socket, response,
            boost::asio::transfer_at_least(1), error))
            std::cout << &response;
        if (error != boost::asio::error::eof)
            throw boost::system::system_error(error);
    }
    catch (std::exception& e)
    {
        std::cout << "Exception: " << e.what() << "\n";
    }

    return 0;
}
