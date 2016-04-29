#!/bin/bash
cd ~/ML_Project/db

sqlite3 so-dump.db 'CREATE TABLE sub_Final AS SELECT  sub_posts_ph.Comment, sub_posts_ph.CreationDate, sub_posts_ph.UserDisplayName, sub_posts_ph.RevisionGUID, sub_posts_ph.UserId, sub_posts_ph.PostId, sub_posts_ph.PostHistoryTypeId, sub_posts_ph.Id, sub_posts_ph."Id:1", sub_posts_ph.Text, sub_posts_ph.Body, sub_posts_ph.ViewCount AS PostViewCount, sub_posts_ph.LastEditorDisplayName, sub_posts_ph.ClosedDate, sub_posts_ph.CommentCount, sub_posts_ph.AnswerCount, sub_posts_ph.AcceptedAnswerId, sub_posts_ph.Score, sub_posts_ph.OwnerDisplayName, sub_posts_ph.Title, sub_posts_ph.PostTypeId, sub_posts_ph.Tags, sub_posts_ph.FavoriteCount, sub_posts_ph.LastActivityDate, sub_posts_ph.delim, users.DownVotes, users.Reputation, users.Views, users.UpVotes, users.CreationDate AS UserCreationDate FROM sub_posts_ph JOIN users ON sub_posts_ph.UserId = users.Id'

sqlite3 so-dump.db ‘ALTER TABLE sub_Final ADD COLUMN Delimiter TEXT DEFAULT "@$R$@" 

sqlite3 so-dump.db ‘ALTER TABLE sub_Final ADD COLUMN CodeSnippet INT DEFAULT 0’
sqlite3 so-dump.db ‘UPDATE sub_Final SET CodeSnippet=1 WHERE Body LIKE "%<code>%"’


sqlite3 so-dump.db ‘ALTER TABLE sub_Final ADD COLUMN PostLength INT DEFAULT NULL’
sqlite3 so-dump.db ‘UPDATE sub_Final SET PostLength=LENGTH(Text) WHERE PostHistoryTypeId = 2’

sqlite3 so-dump.db ‘ALTER TABLE sub_Final ADD COLUMN URLCount INT DEFAULT NULL’
sqlite3 so-dump.db ‘UPDATE sub_Final SET URLCount = (LENGTH(Body) - LENGTH(REPLACE(Body, "</a>", ‘’)))/4 WHERE Body LIKE ("%</a>%") AND PostHistoryTypeId = 2’

sqlite3 so-dump.db ‘ALTER TABLE sub_Final ADD COLUMN PostLifeDays REAL DEFAULT NULL’
sqlite3 so-dump.db ‘UPDATE sub_Final SET PostLifeDays = (julianday("2016-03-01") - julianday(CreationDate)) WHERE PostTypeId = 1’

sqlite3 so-dump.db ‘ALTER TABLE sub_Final ADD COLUMN UserLifeDays REAL DEFAULT NULL’
sqlite3 so-dump.db ‘UPDATE sub_Final SET UserLifeDays = (julianday(CreationDate) - julianday(UserCreationDate)) WHERE PostHistoryTypeId BETWEEN 1 AND 3’
