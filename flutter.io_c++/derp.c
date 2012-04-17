/*
 *
 *  Flutter.io.c
 *  Pre-Interview Question:
 *  must run in gcc/g++ with -O3
 1. Take two arguments, width and height, from the command line
 2. Create an unsigned char matrix M of size width x height
 3. Fill M with random data
 4. Apply [-1, 0, 1] filter along x and y axis (i.e. convolve the image with [-1, 0, 1] kernel along horizontal and vertical axis) in order to compute derivates dx and dy of M along x and y direction respectively (you must explicitly allocate & compute dx & dy matrices)
 5. Compute min and max values for both dx & dy matrices individually
 6. Print total time taken by the machine in computing dx, dy, min and max operations, and print computed min & max values
 *
 *  By Jameson Lee
 */

#include <stdio.h>
#include <stdlib.h>
#include <time.h>

void prettyPrint(int * matrix, int w, int h);
void prettyPrintc(unsigned char * matrix, int w, int h);

inline int max(int a, int b) {
  return (a > b) ? a : b;
}
inline int min(int a, int b) {
  return (a < b) ? a : b;
}

int main(int argc, char ** argv){

  int w,h,wh;
  unsigned char * M;
  int * Mdx;
  int * Mdy;
  int maxdx = 0, maxdy = 0;
  int mindx = 255, mindy = 255;
  unsigned char _t = 0;
  clock_t _start;
  int i = 0;

  if (argc != 3){
    printf("Usage: derp <width> <height>");
    return 0;
  }

  w = atoi(argv[1]);
  h = atoi(argv[2]);
  wh = w*h;

  srand(time(NULL));

  // get more than enough space (buffer for running edge detector)
  M = (unsigned char *) malloc(sizeof(unsigned char)*wh+(2*w));
  Mdx = (int *) malloc(sizeof(int)*wh);
  Mdy = (int *) malloc(sizeof(int)*wh);
  if (!M || !Mdx || !Mdy) {
    printf("Could not allocate enough memory, exiting");
    return 1;
  }

  //make the random matrix
  for(i=w;i<wh+w;i++) M[i] = rand() >> 24;
  prettyPrintc(M,w,h+2);
  // expand the matrix, to loop-linearly
  for(i=0;i<w;i++) {
    M[i] = M[wh+i];
    M[wh+w+i] = M[i+w];
  }
  prettyPrintc(M,w,h+2);
  prettyPrintc(M+w,w,h);

  //dx
  _start = clock();
  for(i=w;i<wh+w;i++) {
    _t = -M[i-1]+M[i+1];
    //maxdx = _t ? maxdx < _t : maxdx;
    //mindx = _t ? mindx > _t : mindx;
    printf("%d, %d, %d\n", -M[i-1],M[i+1],_t);
    Mdx[i] = (int) _t;
  }
  printf("Compute dx: %f\n", (double) (clock()-_start)/CLOCKS_PER_SEC);

  // max dx
  _start = clock();
  for(i=0;i<wh;i++) {
    maxdx = max(maxdx, Mdx[i]);
  }
  printf("Compute max(dx): %f\n", (double) (clock()-_start)/CLOCKS_PER_SEC);
  //printf("Compute max(dx): %f\n", (double) (clock()-_start)/CLOCKS_PER_SEC);

  // min dx
  _start = clock();
  for(i=0;i<wh;i++) {
    mindx = min(mindx, Mdx[i]);
  }
  printf("Compute min(dx): %f\n", (double) (clock()-_start)/CLOCKS_PER_SEC);
 
  //prettyPrint(Mdx,w,h);

  //dy
  for(i=0;i<wh;i++) {
    _t  = -M[i] + M[i+2*w];
    //maxdy = _t ? maxdy < _t : maxdy;
    //mindy = _t ? mindy > _t : mindy;
    Mdy[i] = (int) _t;
  }
  //prettyPrint(Mdy,w,h);
  printf("Compute dy: %f\n", (double) (clock()-_start)/CLOCKS_PER_SEC);

  // max dx
  _start = clock();
  for(i=0;i<wh;i++) {
    maxdy = max(maxdy, Mdy[i]);
  }
  printf("Compute max(dy): %f\n", (double) (clock()-_start)/CLOCKS_PER_SEC);

  // min dx
  _start = clock();
  for(i=0;i<wh;i++) {
    mindy = min(mindy, Mdy[i]);
  }
  printf("Compute min(dy): %f\n", (double) (clock()-_start)/CLOCKS_PER_SEC);

  printf("dx : min( %d ), max ( %d )\n", mindx,maxdx);
  printf("dy : min( %d ), max ( %d )\n", mindy,maxdy);
  prettyPrint(Mdx, w,h);
  prettyPrint(Mdy, w,h);
 
  return 0;
}

void prettyPrint(int * matrix, int w, int h){
  int i,j;
  printf("-----------------------\n");
  for(i=0;i<h;i++){
    for(j=0;j<w;j++){
      printf("%d ",matrix[i*w+j]);
    }
    printf("\n");
  }
}

void prettyPrintc(unsigned char * matrix, int w, int h) {
  int i,j;
  printf("-----------------------\n");
  for(i=0;i<h;i++){
    for(j=0;j<w;j++){
      printf("%d ",matrix[i*w+j]);
    }
    printf("\n");
  }
}
