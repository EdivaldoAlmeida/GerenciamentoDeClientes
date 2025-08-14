--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5
-- Dumped by pg_dump version 17.5

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: clientes; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.clientes (
    id integer NOT NULL,
    nome character varying(255) NOT NULL,
    email character varying(255),
    telefone character varying(20) NOT NULL
);


ALTER TABLE public.clientes OWNER TO postgres;

--
-- Name: clientes_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.clientes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.clientes_id_seq OWNER TO postgres;

--
-- Name: clientes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.clientes_id_seq OWNED BY public.clientes.id;


--
-- Name: emprestimos; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.emprestimos (
    id integer NOT NULL,
    valor_emprestado numeric(10,2) NOT NULL,
    juros_mensal numeric(5,2) NOT NULL,
    num_meses integer NOT NULL,
    detalhes text,
    cliente_telefone character varying(20) NOT NULL,
    valor_parcela numeric(10,2) DEFAULT 0.00 NOT NULL
);


ALTER TABLE public.emprestimos OWNER TO postgres;

--
-- Name: emprestimos_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.emprestimos_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.emprestimos_id_seq OWNER TO postgres;

--
-- Name: emprestimos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.emprestimos_id_seq OWNED BY public.emprestimos.id;


--
-- Name: clientes id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes ALTER COLUMN id SET DEFAULT nextval('public.clientes_id_seq'::regclass);


--
-- Name: emprestimos id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emprestimos ALTER COLUMN id SET DEFAULT nextval('public.emprestimos_id_seq'::regclass);


--
-- Data for Name: clientes; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.clientes (id, nome, email, telefone) FROM stdin;
18	MAN├ë		45455
12	EDIVALDO VIEIRA DE ALMEIDAA	edivaldo.va@gmail.comasfdasdf	89994156683
19	TESTENADO		98098232
14	maria DOUTO	edivaldo.va@gmail.com	899941566837
21	EDIVALDO VIEIRA DE ALMEIDAA	edivaldo.va@gmail.com	89994156232683
22	NOVO MAN├ë		4434343
23	3rqwerwqrewrq		434343
\.


--
-- Data for Name: emprestimos; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.emprestimos (id, valor_emprestado, juros_mensal, num_meses, detalhes, cliente_telefone, valor_parcela) FROM stdin;
11	2300.00	3.00	3	nada a declarar	45455	813.12
12	50000.00	3.00	5		89994156683	10917.73
17	343433.00	3.00	3		89994156683	121413.99
24	2000.00	3.00	4		89994156683	538.05
27	45000.00	3.00	2		98098232	23517.49
10	40000.00	4.00	5		899941566837	8985.08
28	53353.00	5.00	4		899941566837	15046.18
29	34000.00	4.00	7		4434343	5664.73
30	332322.00	4.00	12		434343	35409.63
\.


--
-- Name: clientes_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.clientes_id_seq', 23, true);


--
-- Name: emprestimos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.emprestimos_id_seq', 30, true);


--
-- Name: clientes clientes_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.clientes
    ADD CONSTRAINT clientes_pkey PRIMARY KEY (telefone);


--
-- Name: emprestimos emprestimos_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emprestimos
    ADD CONSTRAINT emprestimos_pkey PRIMARY KEY (id);


--
-- Name: emprestimos emprestimos_cliente_telefone_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.emprestimos
    ADD CONSTRAINT emprestimos_cliente_telefone_fkey FOREIGN KEY (cliente_telefone) REFERENCES public.clientes(telefone);


--
-- PostgreSQL database dump complete
--

