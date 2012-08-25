drop table if exists entries;
create table entries (
  id integer primary key autoincrement,
  title string not null,
  text string not null
);
create table t_test(
  id integer primary key autoincrement,
  name string not null
  );