--
-- PostgreSQL database dump
--

-- Dumped from database version 10.0
-- Dumped by pg_dump version 10.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: Emails; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "Emails" (
    email_id uuid NOT NULL,
    "timestamp" timestamp without time zone NOT NULL
);


--
-- Name: Recipients; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "Recipients" (
    address text NOT NULL,
    email_id uuid NOT NULL,
    CONSTRAINT address_length CHECK ((char_length(address) <= 255))
);


--
-- Name: Words; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE "Words" (
    address text NOT NULL,
    word text NOT NULL,
    count integer DEFAULT 0,
    CONSTRAINT address_length CHECK ((char_length(address) <= 255)),
    CONSTRAINT count_positive CHECK ((count >= 0)),
    CONSTRAINT word_length CHECK ((char_length(word) <= 255))
);


--
-- Name: Emails emails_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "Emails"
    ADD CONSTRAINT emails_pkey PRIMARY KEY (email_id);


--
-- Name: Recipients recipients_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "Recipients"
    ADD CONSTRAINT recipients_pkey PRIMARY KEY (email_id, address);


--
-- Name: Words words_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY "Words"
    ADD CONSTRAINT words_pkey PRIMARY KEY (address, word);


--
-- PostgreSQL database dump complete
--

