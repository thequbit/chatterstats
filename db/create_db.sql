create database chatterstats;

grant usage on chatterstats.* to csuser identified by 'password123%%%';

grant all privileges on chatterstats.* to csuser;

use chatterstats;

create table tweets(
tweetid int not null auto_increment primary key,
username varchar(64) not null,
id varchar(256) not null,
text varchar(256) not null,
created datetime not null,
pulldt datetime not null
);

create index tweets_username on tweets(username);
create index tweets_text on tweets(text);
create index tweets_id on tweets(id);

