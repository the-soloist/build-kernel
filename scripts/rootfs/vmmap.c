/**
 * http://blog.eonew.cn/archives/1162
 *
 * musl-gcc -static vmmap.c -O3 -s -o vmmap
 */
#include <dirent.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

inline static void truncate_string(char *str) {
  while (!(*str == '\n' || *str == '\0')) {
    str++;
  }
  if (*str == '\n') {
    *str = '\0';
  }
}

int main(int argc, char const *argv[]) {
  DIR *dir;
  struct dirent *ptr[0x100], *temp;
  int i, num = 0, text_position = -1;
  FILE *fp;
  char buf[0x400];

  memset(ptr, 0, sizeof(ptr));
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  setvbuf(stderr, NULL, _IONBF, 0);

  if (argc < 2) {
    fprintf(stderr, "Usage: ./vmmap file-path\n");
    exit(1);
  }

  if (chdir(argv[1]) == -1) {
    fprintf(stderr, "chdir error: %m\n");
    exit(1);
  }

  dir = opendir(argv[1]);

  if (dir == NULL) {
    fprintf(stderr, "opendir error: %m\n");
    exit(1);
  }

  for (i = 0; i < 0x100; i++) {
    temp = readdir(dir);
    if (temp == NULL) {
      break;
    }

    if (temp->d_type == DT_REG) {
      if (!strcmp(".text", temp->d_name)) {
        text_position = num;
        ptr[num] = temp;
      } else {
        ptr[num] = temp;
      }
      num++;
    }
  }

  if (text_position == -1) {
    fprintf(stderr, "Error: don't find .text\n");
    exit(1);
  }

  fp = fopen(ptr[text_position]->d_name, "rb");
  if (fp == NULL) {
    fprintf(stderr, "fopen error: %m\n");
    exit(1);
  }
  fgets(buf, 0x400, fp);
  truncate_string(buf);
  printf(" %s ", buf);
  fclose(fp);

  for (i = 0; i < num; i++) {
    if (i == text_position) {
      continue;
    }

    fp = fopen(ptr[i]->d_name, "rb");
    if (fp == NULL) {
      fprintf(stderr, "fopen error: %m\n");
      exit(1);
    }
    fgets(buf, 0x400, fp);
    truncate_string(buf);
    printf("-s %s %s ", ptr[i]->d_name, buf);
    fclose(fp);
  }
  puts("");

  return 0;
}