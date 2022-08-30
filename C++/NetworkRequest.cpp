//
//  NetworkRequest.cpp
//
//  Created by duzixi.com on 15/8/25.
//

#include "NetworkRequest.h"

using namespace std;
using boost::asio::ip::tcp;

void write_log(const std::string& log, const string& str) {
    ofstream file(log, ios_base::app | ios_base::ate | ios_base::out);
    file << str << endl;
    file.close();
}


/// POST����
string PostRequest(const string host, const string path, string form)
{
    // ����Asio����: io_service��������Ȼ���
    boost::asio::io_service io_service;

    // ��ȡ�������ն��б�
    //tcp::resolver resolver(io_service);
    //tcp::resolver::query query("www.baidu.com", "http");
    //tcp::resolver::iterator iter = resolver.resolve(query);

    // ��������ÿһ���նˣ�ֱ���ɹ�����socket����
    tcp::socket socket(io_service);
    //boost::asio::connect(socket, iter);
    socket.connect(tcp::endpoint(boost::asio::ip::address_v4::from_string("XXX.XXX.XXX.XXX"), 22222));
    // ������������ͷ
    // ָ�� "Connection: close" �ڻ�ȡӦ���Ͽ����ӣ�ȷ�����ļ�ȫ�����ݡ�
    boost::asio::streambuf request;
    ostream request_stream(&request);
    request_stream << "POST " << path << " HTTP/1.1\r\n";
    request_stream << "Host: " << host << "\r\n";
    request_stream << "Accept: */*\r\n";
    request_stream << "Content-Type:application/json\r\n";
    request_stream << "Content-Length: " << form.length() << "\r\n";
    request_stream << "Connection: close\r\n\r\n"; // ע����������������
    request_stream <<form; //POST ���͵����ݱ����������ڿ���

    // ��������
    boost::asio::write(socket, request);

    // ��ȡӦ��״̬. Ӧ�𻺳��� streambuf ���Զ���������������
    // �����������ڹ��컺����ʱͨ���������ֵ����
    boost::asio::streambuf response;
    boost::asio::read_until(socket, response, "\r\n");

    // ���Ӧ���Ƿ�OK.
    istream response_stream(&response);// Ӧ����
    string http_version;
    response_stream >> http_version;
    unsigned int status_code;
    response_stream >> status_code;
    string status_message;
    getline(response_stream, status_message);
    if (!response_stream || http_version.substr(0, 5) != "HTTP/")
    {
        printf("��Ч��Ӧ\n");
    }
    if (status_code != 200)
    {
        printf("��Ӧ���� status code %d\n", status_code);
    }

    // ��ȡӦ��ͷ�����������к�ֹͣ
    boost::asio::read_until(socket, response, "\r\n\r\n");

    // ��ʾӦ��ͷ��
    string header;
    int len = 0;
    while (getline(response_stream, header) && header != "\r")
    {
        if (header.find("Content-Length: ") == 0) {
            stringstream stream;
            stream << header.substr(16);
            stream >> len;
        }
    }

    long size = response.size();

    if (size > 0) {
        // .... do nothing
    }

    // ѭ����ȡ��������ֱ���ļ�����
    boost::system::error_code error;
    while (boost::asio::read(socket, response, boost::asio::transfer_at_least(1), error))
    {
        // ��ȡӦ�𳤶�
        size = response.size();
        if (len != 0) {
            cout << size << "  Byte  " << (size * 100) / len << "%\n";
        }

    }
    if (error != boost::asio::error::eof)
    {
        throw boost::system::system_error(error);
    }

    cout << size << " Byte �������������." << endl;

    // ��streambuf����ת��Ϊstring���ͷ���
    istream is(&response);
    is.unsetf(ios_base::skipws);
    string sz;
    sz.append(istream_iterator<char>(is), istream_iterator<char>());
    std::cout << sz << std::endl;
    write_log("log.txt", sz);
    // ����ת������ַ���
    return sz;
}


/// GET����
string GetRequest(char* host, char* path)
{
    // ����Asio����: io_service��������Ȼ���
    boost::asio::io_service io_service;

    // ��ȡ�������ն��б�
    tcp::resolver resolver(io_service);
    tcp::resolver::query query(host, "http");
    tcp::resolver::iterator iter = resolver.resolve(query);

    // ��������ÿһ���նˣ�ֱ���ɹ�����socket����
    tcp::socket socket(io_service);
    boost::asio::connect(socket, iter);

    // ������������ͷ.
    // ָ�� "Connection: close" �ڻ�ȡӦ���Ͽ����ӣ�ȷ�����ļ�ȫ�����ݡ�
    boost::asio::streambuf request;
    ostream request_stream(&request);
    request_stream << "GET " << path << " HTTP/1.1\r\n";
    request_stream << "Host: " << host << "\r\n";
    request_stream << "Accept: */*\r\n";
    request_stream << "Connection: close\r\n\r\n";

    // ��������
    boost::asio::write(socket, request);

    // ��ȡӦ��״̬. Ӧ�𻺳��� streambuf ���Զ���������������
    // �����������ڹ��컺����ʱͨ���������ֵ����
    boost::asio::streambuf response;
    boost::asio::read_until(socket, response, "\r\n");

    // ���Ӧ���Ƿ�OK.
    istream response_stream(&response);
    string http_version;
    response_stream >> http_version;
    unsigned int status_code;
    response_stream >> status_code;
    string status_message;
    getline(response_stream, status_message);
    if (!response_stream || http_version.substr(0, 5) != "HTTP/")
    {
        printf("��Ӧ��Ч\n");
    }
    if (status_code != 200)
    {
        printf("��Ӧ���� status code %d\n", status_code);
    }

    // ��ȡӦ��ͷ�����������к�ֹͣ
    boost::asio::read_until(socket, response, "\r\n\r\n");

    // ��ʾӦ��ͷ��

    string header;
    int len = 0;
    while (getline(response_stream, header) && header != "\r")
    {
        if (header.find("Content-Length: ") == 0) {
            stringstream stream;
            stream << header.substr(16);
            stream >> len;
        }
    }

    long size = response.size();

    if (size > 0) {
        // ... do nothing ...
    }

    boost::system::error_code error;  // ��ȡ����

    // ѭ����ȡ��������ֱ���ļ�����
    while (boost::asio::read(socket, response, boost::asio::transfer_at_least(1), error))
    {
        // ��ȡӦ�𳤶�
        size = response.size();
        if (len != 0) {
            cout << size << "  Byte  " << (size * 100) / len << "%" << endl;
        }
    }

    // ���û�ж����ļ�β���׳��쳣
    if (error != boost::asio::error::eof)
    {
        throw boost::system::system_error(error);
    }

    cout << size << " Byte �������������." << endl;

    // ��streambuf����ת��Ϊstring���ͣ�������
    istream is(&response);
    is.unsetf(ios_base::skipws);
    string sz;
    sz.append(istream_iterator<char>(is), istream_iterator<char>());

    return sz;
}

/// GET����(����)
string GetRequest(string url)
{
    size_t index;

    // ȥ��url�е�Э��ͷ
    if (url.find("http://") != string::npos) {
        url = url.substr(7);
    }
    printf("url:%s\n", url.c_str());

    // ��ȡhost�ַ���
    index = url.find("/");
    char* host = new char[index];
    strcpy(host, url.substr(0, index).c_str());

    // ��ȡurlPath�ַ���
    char* urlPath = new char[url.length() - index + 1];
    strcpy(urlPath, url.substr(index, url.length() - index).c_str());

    return GetRequest(host, urlPath);
}

int main() {
    boost::json::value jv = {
        { "keyWord", "18"},
        { "limitCount", 5 },
    };
    PostRequest("10.141.44.20:19990", "/qm/query/trade", boost::json::serialize(jv));
}