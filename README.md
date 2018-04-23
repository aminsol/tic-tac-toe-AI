SET @exp = (SELECT count(*) FROM `longterm` where `explored` = 1 limit 1),
@total =(SELECT count(*) FROM `longterm` limit 1);

SELECT @exp/@total as full_train;