/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2011/12/5 23:26:43                           */
/*==============================================================*/


drop table if exists c2_files;

drop table if exists c2_log;

drop table if exists c2_project;

drop table if exists c2_revision;

drop table if exists c2_server;

/*==============================================================*/
/* Table: c2_files                                              */
/*==============================================================*/
create table c2_files
(
   f_id                 int not null auto_increment,
   r_id                 int,
   f_path               varchar(250) not null,
   f_ver                varchar(10) not null,
   primary key (f_id)
);

/*==============================================================*/
/* Table: c2_log                                                */
/*==============================================================*/
create table c2_log
(
   h_id                 int not null auto_increment,
   r_no                 varchar(30) not null,
   p_id                 int,
   s_id                 int,
   s_name               varchar(30) not null,
   r_dateline           int not null,
   primary key (h_id)
);

/*==============================================================*/
/* Table: c2_project                                            */
/*==============================================================*/
create table c2_project
(
   p_id                 int not null auto_increment,
   p_name               varchar(20) not null,
   p_path               varchar(120) not null,
   p_user               varchar(30) not null,
   p_pass               varchar(30) not null,
   p_status             tinyint not null default 0,
   p_cdateline          int not null,
   primary key (p_id)
);

/*==============================================================*/
/* Table: c2_revision                                           */
/*==============================================================*/
create table c2_revision
(
   r_id                 int not null auto_increment,
   p_id                 int,
   r_no                 varchar(30) not null,
   s_id                 int,
   s_name               varchar(30) not null,
   r_dateline           int not null,
   r_cdateline          int not null,
   primary key (r_id)
);

/*==============================================================*/
/* Table: c2_server                                             */
/*==============================================================*/
create table c2_server
(
   s_id                 int not null auto_increment,
   p_id                 int,
   s_name               varchar(30) not null,
   s_host               char(15) not null,
   s_user               varchar(30) not null,
   s_pass               varchar(30) not null,
   s_status             tinyint not null,
   s_cdateline          int not null,
   primary key (s_id)
);
