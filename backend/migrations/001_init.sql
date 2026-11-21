CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TABLE IF NOT EXISTS organizations (
 id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
 name text NOT NULL,
 slug text UNIQUE NOT NULL,
 created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS leads (
 id uuid PRIMARY KEY,
 organization_id uuid NOT NULL REFERENCES organizations(id) ON DELETE CASCADE,
 student_name varchar(100) NOT NULL,
 phone varchar(20) NOT NULL,
 email text,
 source text NOT NULL DEFAULT 'other' CHECK (source IN ('website','whatsapp','instagram','referral','walk_in','other')),
 status text NOT NULL DEFAULT 'new' CHECK (status IN ('new','contacted','interested','enrolled','lost')),
 notes varchar(2000),
 consent_to_contact boolean NOT NULL DEFAULT false,
 created_at timestamptz NOT NULL DEFAULT now(),
 updated_at timestamptz NOT NULL DEFAULT now()
);
CREATE INDEX IF NOT EXISTS leads_org_created_idx ON leads(organization_id,created_at DESC);
