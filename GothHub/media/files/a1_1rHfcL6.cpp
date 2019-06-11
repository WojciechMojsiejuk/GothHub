#include<iostream>
#include<cstdio>
#include <fstream>
#include <cstdlib>
#include<string>
using namespace std;

int NWP_alg(string X, string Y)
{
    int tu; 
	int zmiany;
	int a;
    int NWP[n+1][m+1];
    for(int i=0;i<n+1;i++)
        for(int j=0;j<m+1;j++)
            NWP[i][j] = 0;
    for(int i=0;i<n;i++)
        for(int j=0;j<m;j++)
        if(X[i]==Y[j])
            NWP[i+1][j+1]=NWP[i][j]+1;
            else
            {
                if(NWP[i][j+1] > NWP[i+1][j]) NWP[i+1][j+1]=NWP[i][j+1];
                else NWP[i+1][j+1]=NWP[i+1][j];
            }
    return NWP[n][m];
}

int main() {
    int n;
    string slowo[100];
    fstream plik_we;
    plik_we.open("In0301.txt", ios::in);
    if(plik_we.good()==false) cout<<"Nie mozna otworzyc pliku!";
    plik_we >> n;
    for(int i = 0; i < 2*n; i ++)
    {
        plik_we >> slowo[i];
    }
    plik_we.close();
    //zapis
    fstream plik_wy;
    plik_wy.open("Out0301.txt",ios::out);
    for(int i = 0; i < 2*n; i+=2){
    	plik_wy << NWP_alg(slowo[i], slowo[i+1]) << endl;
	}
        
    plik_wy.close();
}
