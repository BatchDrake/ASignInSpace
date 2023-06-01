#include <stdio.h>

int
main(void)
{
  int i, c;

  while ((c = getchar()) != EOF)
    for (i = 0; i < 8; ++i)
      putchar('0' | !!(c & (1 << 7 - i)));
  
  return 0;
}
