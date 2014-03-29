-- admin
INSERT INTO permissions(name) VALUES('admin');

-- admin has all moderator permissions
INSERT INTO permissions(name, parent) VALUES('moderator', 'admin');

-- other admin permissions
INSERT INTO permissions(name, parent) VALUES('manage_moderator', 'admin');
INSERT INTO permissions(name, parent) VALUES('manage_role', 'admin');

-- moderator permissions
INSERT INTO permissions(name, parent) VALUES('manage_article', 'moderator');
INSERT INTO permissions(name, parent) VALUES('manage_comment', 'moderator');
INSERT INTO permissions(name, parent) VALUES('manage_user', 'moderator');

-- moderator has all contributor permissions
INSERT INTO permissions(name, parent) VALUES('contributor', 'moderator');

-- contributor permissions
INSERT INTO permissions(name, parent) VALUES('create_article', 'contributor');

-- contributor has all user permissions
INSERT INTO permissions(name, parent) VALUES('user', 'contributor');

-- user permissions
INSERT INTO permissions(name, parent) VALUES('view_online_user', 'user');

-- article related permissions
INSERT INTO permissions(name, parent) VALUES('delete_article', 'manage_article');
INSERT INTO permissions(name, parent) VALUES('update_article', 'manage_article');
INSERT INTO permissions(name, parent) VALUES('approve_article', 'manage_article');

-- moderator related permissions
INSERT INTO permissions(name, parent) VALUES('add_moderator', 'manage_moderator');
INSERT INTO permissions(name, parent) VALUES('remove_moderator', 'manage_moderator');

-- comment related permissions
INSERT INTO permissions(name, parent) VALUES('delete_comment', 'manage_comment');
INSERT INTO permissions(name, parent) VALUES('update_comment', 'manage_comment');

-- roles
INSERT INTO permissions(name, parent) VALUES('create_role', 'manage_role');
INSERT INTO permissions(name, parent) VALUES('delete_role', 'manage_role');

-- user related permissions
INSERT INTO permissions(name, parent) VALUES('ban_user', 'manage_user');
INSERT INTO permissions(name, parent) VALUES('unban_user', 'manage_user');