document.addEventListener('alpine:init', () => {
    Alpine.data('modal', () => ({
        visible: false,
        user: null,
        action: null,
        message: null,
        open(message) {
            this.message = message
            this.visible = true
        },
        close() {
            this.visible = false
            this.user = null
        },
        activate(e) {
            this.user = e.target.dataset.user
            this.open("Voulez-vous vraiment activer cet utilisateur ?")
            this.action = 'activate'
        },
        deactivate(e) {
            this.user = e.target.dataset.user
            this.open("Voulez-vous vraiment désactiver cet utilisateur ?")
            this.action = 'deactivate'
        },
        deleteUser(e) {
            this.user = e.target.dataset.user
            this.open("Vous-vous vraiment supprimer cet utilisateur ?")
            this.action = 'delete'
        },
        submit(e) {
            e.target.action = `/admin/${this.action}/users/${this.user}`
            e.target.submit()
        }
    }))
})