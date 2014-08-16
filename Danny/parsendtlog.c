/*
 * parsendtlog.c
 *
 * Parses the snaplog and prints everything out
 *
 * Author: Danny Lee (dannylee@gatech.edu)
 */

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <libgen.h>
#include <string.h>
#include "web100.h"

#define PRINT_CSV_HEADER 1

int main(int argc, char **argv)
{
  web100_agent      *agent;
  web100_group      *group;
  web100_snapshot   *snap;
  web100_log 	    *log;
  web100_var 	    *var = NULL;
  time_t	    log_time;

  char *filename;
  const char *ext;
  char *name;

  int data_direction = 0;
  int last_entry = 0;

  /*
  web100_connection *conn;
  struct web100_connection_spec spec;
  unsigned char *src;
  unsigned char *dst;
  int cid;
  */

  char buf[32];

  // Error check the input file
  if (argc != 2)
    printf("Usage: %s <snaplog>\n", argv[0]);

  // extract filename from input path
  filename = basename(argv[1]);

  // extract extension and name from filename
  ext = strrchr(filename, '.');
  name = malloc(ext - filename + 1);
  strncpy(name, filename, ext - filename);

  // We're looking for a snaplog file, c2s or s2c
  if (strcmp(ext+1, "c2s_snaplog")) {
    data_direction = 0;
  }
  else if (strcmp(ext+1, "s2c_snaplog")) {
    data_direction = 1;
  }
  else {
    printf("Error: unknown file extension %s", ext+1);
    free(name);
    exit(EXIT_FAILURE);
  }

  // Step 1: Build the CSV format string
  // Remove definition of PRINT_CSV_HEADER if you want to skip this
#ifdef PRINT_CSV_HEADER
  // Open for reading
  log = web100_log_open_read(argv[1]);
  if (log == NULL) {
    web100_perror("web100_log_open_read");      
    exit(EXIT_FAILURE);
  }

  group = web100_get_log_group(log);
  snap = web100_snapshot_alloc_from_log(log);
  if (snap == NULL)
    web100_perror("web100_snap_read");

  printf("test_id,log_time,data_direction,");
  var = web100_var_head(group);
  while (var) {
    if (web100_snap_read(var, snap, buf)) {
      web100_perror("web100_snap_read");
      exit(EXIT_FAILURE);
    }
    printf("%s,",web100_get_var_name(var));
    var = web100_var_next(var);
  }
  printf("is_last_entry\n");

  web100_snapshot_free(snap);

  // Close to reset all pointers
  web100_log_close_read(log);
#endif    

  // Step 2: Parse all the variables and print them out as csv

  // Open for reading
  log = web100_log_open_read(argv[1]);
  if (log == NULL) {
    web100_perror("web100_log_open_read");    
    free(name);
    exit(EXIT_FAILURE);
  }

  // Get info about the session
  //agent = web100_get_log_agent(log);
  group = web100_get_log_group(log);
  log_time = web100_get_log_time(log);

  /* might need this later
  conn = web100_get_log_connection(log);
  cid = web100_get_connection_cid(conn);
  web100_get_connection_spec(conn, &spec);
  */

  snap = web100_snapshot_alloc_from_log(log);
  if (snap == NULL) {
    web100_perror("web100_snapshot_alloc_from_log");
    free(name);
    exit(EXIT_FAILURE);
  }
  web100_snap_from_log(snap, log);
  while (snap != NULL && last_entry != 1) {
    printf("%s,%u,%u,",
	   name,
	   log_time,
	   data_direction);

    var = web100_var_head(group);
    while (var) {
      if (web100_snap_read(var, snap, buf)) {
	web100_perror("web100_snap_read");
	free(name);
	exit(EXIT_FAILURE);
      }
      printf("%s,",web100_value_to_text(web100_get_var_type(var), buf));
      var = web100_var_next(var);
    }
    // get next and check if we've hit the last entry
    if (web100_snap_from_log(snap, log) != 0)
      last_entry = 1;

    printf("%u\n",last_entry);
  }

  // cleanup
  web100_snapshot_free(snap);
  web100_log_close_read(log);
  free(name);
  return;
}

