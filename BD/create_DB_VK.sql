-- DROP SCHEMA public;

CREATE SCHEMA public AUTHORIZATION pg_database_owner;

COMMENT ON SCHEMA public IS 'standard public schema';

-- DROP SEQUENCE public.applicants_id_seq;

CREATE SEQUENCE public.applicants_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.favorites_id_seq;

CREATE SEQUENCE public.favorites_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE public.users_id_seq;

CREATE SEQUENCE public.users_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- public.users definition

-- Drop table

-- DROP TABLE public.users;

CREATE TABLE public.users (
	id serial4 NOT NULL,
	id_vk_users int4 NOT NULL,
	sex varchar(30) NOT NULL,
	age varchar(30) NOT NULL,
	city varchar(50) NOT NULL,
	CONSTRAINT users_id_vk_users_key UNIQUE (id_vk_users),
	CONSTRAINT users_pkey PRIMARY KEY (id)
);


-- public.applicants definition

-- Drop table

-- DROP TABLE public.applicants;

CREATE TABLE public.applicants (
	id serial4 NOT NULL,
	id_user int4 NOT NULL,
	id_vk_applicant int4 NOT NULL,
	photo_1 varchar NOT NULL,
	photo_2 varchar NOT NULL,
	photo_3 varchar NOT NULL,
	CONSTRAINT applicants_id_vk_applicant_key UNIQUE (id_vk_applicant),
	CONSTRAINT applicants_pkey PRIMARY KEY (id),
	CONSTRAINT applicants_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id)
);


-- public.favorites definition

-- Drop table

-- DROP TABLE public.favorites;

CREATE TABLE public.favorites (
	id serial4 NOT NULL,
	id_user int4 NOT NULL,
	id_vk_favorite int4 NOT NULL,
	photo_1 varchar NOT NULL,
	photo_2 varchar NOT NULL,
	photo_3 varchar NOT NULL,
	CONSTRAINT favorites_id_vk_favorite_key UNIQUE (id_vk_favorite),
	CONSTRAINT favorites_pkey PRIMARY KEY (id),
	CONSTRAINT favorites_id_user_fkey FOREIGN KEY (id_user) REFERENCES public.users(id)
);
