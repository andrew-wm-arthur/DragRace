#!/bin/bash
cd ~/ML_Project/db

sqlite3 so-dump.db "CREATE TABLE posts_ph AS SELECT 
		posthistory.Comment,
		posthistory.CreationDate,
		posthistory.UserDisplayName,
		posthistory.RevisionGUID,
		posthistory.UserId,
		posthistory.PostId,
		posthistory.PostHistoryTypeId,
		posthistory.Id,
		posthistory.Text,
		posts.Body,
		posts.ViewCount,
		posts.LastEditorDisplayName,
		posts.ClosedDate,
		posts.CommentCount,
		posts.AnswerCount,
		posts.AcceptedAnswerId,
		posts.Score,
		posts.OwnerDisplayName,
		posts.Title,
		posts.PostTypeId,
		posts.Tags,
		posts.CreationDate,
		posts.FavoriteCount,
		posts.LastActivityDate,
		posts.Id 
	FROM posts JOIN posthistory ON posts.Id = posthistory.PostId";

sqlite3 so-dump.db 'CREATE TABLE FinalTable AS SELECT 
		posts_ph.Comment,
		posts_ph.CreationDate,
		posts_ph.UserDisplayName,
		posts_ph.RevisionGUID,
		posts_ph.UserId,
		posts_ph.PostId,
		posts_ph.PostHistoryTypeId,
		posts_ph.Id,
		posts_ph."Id:1"
		posts_ph.Text,
		posts_ph.Body,
		posts_ph.ViewCount AS PostViewCount,
		posts_ph.LastEditorDisplayName,
		posts_ph.ClosedDate,
		posts_ph.CommentCount,
		posts_ph.AnswerCount,
		posts_ph.AcceptedAnswerId,
		posts_ph.Score,
		posts_ph.OwnerDisplayName,
		posts_ph.Title,
		posts_ph.PostTypeId,
		posts_ph.Tags,
		posts_ph.FavoriteCount,
		posts_ph.LastActivityDate,
		users.DownVotes,
		users.Reputation,
		users.Views,
		users.UpVotes,
		users.CreationDate AS UserCreationDate 
	FROM posts_ph JOIN users ON posts_ph.UserId = users.Id';

sqlite3 so-dump.db ‘ALTER TABLE FinalTable ADD COLUMN Delimiter TEXT DEFAULT ‘@$R$@’;

sqlite3 so-dump.db ‘ALTER TABLE FinalTable ADD COLUMN CodeSnippet INT DEFAULT 0’;
sqlite3 so-dump.db ‘UPDATE FinalTable SET CodeSnippet=1 WHERE Body LIKE ‘%<code>%’’;


sqlite3 so-dump.db ‘ALTER TABLE FinalTable ADD COLUMN PostLength INT DEFAULT NULL’;
sqlite3 so-dump.db ‘UPDATE FinalTable SET PostLength=LENGTH(Text) WHERE PostHistoryTypeId = 2’;

sqlite3 so-dump.db ‘ALTER TABLE FinalTable ADD COLUMN URLCount INT DEFAULT NULL’;
sqlite3 so-dump.db ‘UPDATE FinalTable SET URLCount = (LENGTH(Body) - LENGTH(REPLACE(Body, ‘</a>’, ‘’)))/4 WHERE Body LIKE (‘%</a>%’) AND PostHistoryTypeId = 2’;

sqlite3 so-dump.db ‘ALTER TABLE FinalTable ADD COLUMN PostLifeDays REAL DEFAULT NULL’;
sqlite3 so-dump.db ‘UPDATE FinalTable SET PostLifeDays = (julianday(‘2016-03-01’) - julianday(CreationDate)) WHERE PostTypeId = 1’;

sqlite3 so-dump.db ‘ALTER TABLE FinalTable ADD COLUMN UserLifeDays REAL DEFAULT NULL’;
sqlite3 so-dump.db ‘UPDATE FinalTable SET UserLifeDays = (julianday(CreationDate) - julianday(UserCreationDate)) WHERE PostHistoryTypeId BETWEEN 1 AND 3’;
