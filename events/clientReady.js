const { emptyDir } = require('fs-extra');

module.exports = {
    name: 'ready',
    once: true,
    async execute(login) {
        console.log(`Logged in as ${login.user.tag}`);

        await emptyDir('music');
    }
}
