#include "stdio.h"
#include "stdlib.h"
#include "string.h"

#define BLACKLIST_FILE "d:\\dummy_ip.bin"//一个512MB大小的随机内容的二进制文件

char *test=new char[512*1024*1024];//IP地址映射到本地内存数据的数组
int init();
bool checkBlackList(unsigned long inputIP);
void setValue(unsigned long inputIP, bool inputValue);

//全IP段IP黑名单快速查询

//原理：IP从0.0.0.0到255.255.255.255，总共2^32个IP地址。每个IP地址只有两个状态：在黑名单，或者不在
//因此最初设计是申请0x00000000到0xFFFFFFFF个字节的内存空间（4GB），建立全IP地址到内存的映射，每个字节存放一个二进位，存储该地址对应IP是不是黑名单IP
//经过压缩之后，每个字节存放8个二进制位，因此总空间可压缩到原先的八分之一，即512MB
//查询时，将IP地址的四个字节合组成一个int32并右移3位，得到该IP对应的字节，然后用这个int32的低三位确定字节里的二进制位，即是否是黑名单IP
//将IP转换成int32之后，单次查询仅需要1次内存直接访问和3次位操作
//适用于IP黑名单很大的情况

int main(int argc, char* argv[])
{
    init();
    for(int i=0;i<100;++i)
    {    //生成随机的IP地址进行查询
        unsigned char a=rand()%256,b=rand()%256,c=rand()%256,d=rand()%256;
        unsigned long ip=a*b*c*d;
        printf("IP:%u.%u.%u.%u is hit:%d\n",a,b,c,d,checkBlackList(ip));
    }
    return 0;
}

//数据初始化，将保存在本地文件的数据读取到内存里
int init()
{
    FILE* fp = fopen(BLACKLIST_FILE,"r");
    if (fp==NULL)
        return 0;
    fgets(test,strlen(test),fp);
    fclose(fp);
    return 1;
}

//查询IP是否在黑名单里，仅仅需要三次位运算和一次内存访问
bool checkBlackList(unsigned long inputIP)
{
    return test[inputIP>>3] &(1<<(inputIP & (unsigned long)7));
}

//设置黑名单IP的值。找到IP对应的字节，然后使用掩码和位运算设置对应的二进制位的值
void setValue(unsigned long inputIP, bool inputValue)
{
    unsigned long byteIndex = inputIP >> 3;
    char maskByte = (char)(1<<(inputIP & (unsigned long)7));
    test[byteIndex] = (inputValue?(test[byteIndex] | maskByte):(test[byteIndex] & (!maskByte)));
    /*if(inputValue)//喜欢简洁，改成(:?)形式了，见上行
        test[byteIndex] = test[byteIndex] | maskByte;
    else
        test[byteIndex] = test[byteIndex] & (!maskByte);*/
}
