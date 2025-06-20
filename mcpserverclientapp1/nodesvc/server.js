const express = require('express');
const fs = require('fs');
const path = require('path');

const app = express();
const PORT = 3000;

app.get('/users', (req, res) => {
  const usersPath = path.join(__dirname, 'users.json');
  const users = JSON.parse(fs.readFileSync(usersPath, 'utf8'));
  res.json(users);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});