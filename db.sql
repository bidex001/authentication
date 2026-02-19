--
-- PostgreSQL database dump
--

\restrict cWOyLcgTuZHXTsHSVWffDp2TtbSmDOWWTL8DSprzbUnkfpmqRP3DAy7Ssv5UuAt

-- Dumped from database version 18.1
-- Dumped by pg_dump version 18.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: role_enum; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.role_enum AS ENUM (
    'admin',
    'customer',
    'vendor'
);


ALTER TYPE public.role_enum OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: cart_items; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cart_items (
    id uuid NOT NULL,
    item_id uuid NOT NULL,
    quantity integer,
    cart_id uuid NOT NULL
);


ALTER TABLE public.cart_items OWNER TO postgres;

--
-- Name: carts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.carts (
    id uuid NOT NULL,
    user_id uuid NOT NULL
);


ALTER TABLE public.carts OWNER TO postgres;

--
-- Name: products; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.products (
    "productId" uuid NOT NULL,
    name character varying NOT NULL,
    price numeric NOT NULL,
    description character varying,
    available integer NOT NULL,
    vendor_id uuid NOT NULL
);


ALTER TABLE public.products OWNER TO postgres;

--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    user_id uuid NOT NULL,
    "userName" character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    otp integer,
    "otpExpiry" timestamp with time zone,
    role public.role_enum NOT NULL,
    token_version integer NOT NULL,
    created_at timestamp with time zone DEFAULT now(),
    updated_at timestamp with time zone
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Data for Name: cart_items; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.cart_items (id, item_id, quantity, cart_id) FROM stdin;
cfd8891b-a510-46d6-8650-f2cfb28e534f	25367162-6b09-44b6-800a-63fe64c40d93	100	b9fc5f3b-38e2-4d97-aac9-557b05ea13b7
\.


--
-- Data for Name: carts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.carts (id, user_id) FROM stdin;
b9fc5f3b-38e2-4d97-aac9-557b05ea13b7	777aa447-e968-44f4-8072-ce04ab36e21e
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.products ("productId", name, price, description, available, vendor_id) FROM stdin;
9565d590-fa14-4a17-b65a-a8d8e49409ea	leather	40.98	is good for the health	40	777aa447-e968-44f4-8072-ce04ab36e21e
f71be956-0a42-4b77-b20b-06d43394ae3f	leath	40.98	is good for the health	50	777aa447-e968-44f4-8072-ce04ab36e21e
25367162-6b09-44b6-800a-63fe64c40d93	leat	40.98	is good for the health	200	777aa447-e968-44f4-8072-ce04ab36e21e
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (user_id, "userName", email, password, otp, "otpExpiry", role, token_version, created_at, updated_at) FROM stdin;
777aa447-e968-44f4-8072-ce04ab36e21e	benivendor1234878	beniciyyuitty604@580	$argon2id$v=19$m=65536,t=3,p=4$+l9L6R0jpFRKqRWCUEoJoQ$almci7UrfK+50nH30GP4JgzJL17Ob0bfewC8tXaJAno	3519	2026-02-13 12:27:13.4704+01	vendor	0	2026-02-13 12:21:34.651941+01	2026-02-13 12:22:37.632928+01
\.


--
-- Name: cart_items cart_items_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_pkey PRIMARY KEY (id);


--
-- Name: carts carts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY ("productId");


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- Name: users users_userName_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT "users_userName_key" UNIQUE ("userName");


--
-- Name: cart_items cart_items_cart_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_cart_id_fkey FOREIGN KEY (cart_id) REFERENCES public.carts(id);


--
-- Name: cart_items cart_items_item_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cart_items
    ADD CONSTRAINT cart_items_item_id_fkey FOREIGN KEY (item_id) REFERENCES public.products("productId");


--
-- Name: carts carts_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.carts
    ADD CONSTRAINT carts_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- Name: products products_vendor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_vendor_id_fkey FOREIGN KEY (vendor_id) REFERENCES public.users(user_id);


--
-- PostgreSQL database dump complete
--

\unrestrict cWOyLcgTuZHXTsHSVWffDp2TtbSmDOWWTL8DSprzbUnkfpmqRP3DAy7Ssv5UuAt

