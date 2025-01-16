START TRANSACTION;


-- Insert values into items
INSERT INTO items (id, item_index, level, item_type, item_content, name)
VALUES
(1, 1, 1, 'document', '/static/1doc.png', 'Document'),
(2, 2, 1, 'letter', '/static/1report.jpg', 'Report'),
(3, 3, 1, 'photograph', '/static/1autopsy.jpg', 'Autopsy'),
(4, 4, 1, 'letter', '/static/1letter.jpg', 'Letter'),
(8, 3, 1, 'photograph', '/static/1key.png', 'Locker key');

COMMIT;
