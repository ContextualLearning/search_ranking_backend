create table users (
  user_id integer not null auto_increment,
  uniqname varchar(128) not null unique,
  primary key(user_id)
)Engine=Innodb default charset utf8;

create table topics (
  topic_id integer not null auto_increment,
  title varchar(128) not null,
  primary key(topic_id)
)Engine=Innodb default charset utf8;

create table video_clips (
  clip_id integer not null,
  embed_link text,
  transcript text,
  topic_id integer not null,
  primary key(clip_id),
  foreign key(topic_id) references topics(topic_id) on update cascade on delete cascade
)Engine=Innodb default charset utf8;

create table questions (
  question_id integer not null auto_increment,
  topic_id integer not null,
  option_1_id integer not null,
  option_2_id integer not null,
  option_3_id integer not null,
  option_4_id integer not null,
  primary key(question_id),
  foreign key(option_1_id) references video_clips(clip_id) on update cascade on delete cascade,
  foreign key(option_2_id) references video_clips(clip_id) on update cascade on delete cascade,
  foreign key(option_3_id) references video_clips(clip_id) on update cascade on delete cascade,
  foreign key(option_4_id) references video_clips(clip_id) on update cascade on delete cascade,
  foreign key(topic_id) references topics(topic_id) on update cascade on delete cascade
)Engine=Innodb default charset utf8;

create table user_question (
  user_id integer not null,
  question_id integer not null,
  best_option integer,
  worst_option integer,
  primary key(user_id, question_id),
  foreign key(user_id) references users(user_id) on update cascade on delete cascade,
  foreign key(question_id) references questions(question_id) on update cascade on delete cascade
)Engine=Innodb default charset utf8;
