const extra = require('fs-extra');

module.exports = {
    name: 'ready',
    once: true,
    async execute(login) {
        console.log(`Logged in as ${login.user.tag}`);

        await extra.emptyDir('music');
    }
}
