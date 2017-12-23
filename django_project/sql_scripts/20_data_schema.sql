-- DROP SCHEMA IF EXISTS data CASCADE;
CREATE SCHEMA IF NOT EXISTS data;

CREATE TABLE data.changeset (
    id serial primary key,

    ts_created timestamp with time zone default now(),
    webuser_id integer not null
);

CREATE TABLE data.feature (
    id serial not null,
    name varchar(100) NOT NULL,
    point_geometry GEOMETRY(Point, 4326) NOT NULL,
    overall_assessment INTEGER DEFAULT 1,
    changeset_id INTEGER NOT NULL
);

alter table data.feature
    add primary key (id);

create index ix_feature_pk
    on
        data.feature
        using
        btree (id);

CREATE INDEX ix_feature_point_geometry
    ON data.feature (point_geometry);


CREATE TABLE data.attribute_group (
    id serial PRIMARY KEY,
    name varchar(128) not null,
    position integer not null
);


CREATE TYPE data.type_result AS ENUM('Integer', 'Decimal', 'DropDown', 'MultipleChoice');

CREATE TABLE data.attribute (
    id serial PRIMARY KEY,
    name VARCHAR(128) not null,
    result_type data.type_result,
    attribute_group_id integer not null
);

ALTER TABLE data.attribute ADD CONSTRAINT fk_attribute_attribute_group
    FOREIGN KEY (attribute_group_id) REFERENCES data.attribute_group (id);


CREATE TABLE data.feature_attribute_value
(
    id serial,

    val_text character varying(32),
    val_int int,
    val_real numeric(9,2),

    feature_id integer NOT NULL,
    attribute_id integer NOT null,
    changeset_id integer NOT NULL,

    ts timestamp with time zone default now()
);

alter table data.feature_attribute_value
    add primary key (feature_id, attribute_id, changeset_id);

create index ix_feature_attributes_value_pk
    on
        data.feature_attribute_value
        using
        btree (feature_id, attribute_id, changeset_id);
