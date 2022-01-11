document.addEventListener('alpine:init', () => {
    Alpine.data('modal', () => ({
        visible: false,
        item: null,
        type: null,
        action: null,
        open() {
            this.visible = true
        },
        close() {
            this.visible = false
            this.item = null
        },
        activate(e) {
            this.item = e.target.dataset.id
            this.type = e.target.dataset.type
            this.action = 'activate'
            this.open()
        },
        deactivate(e) {
            this.item = e.target.dataset.id
            this.type = e.target.dataset.type
            this.action = 'deactivate'
            this.open()
        },
        deleteItem(e) {
            this.item = e.target.dataset.id
            this.type = e.target.dataset.type
            this.action = 'delete'
            this.open()
        },
        submit(e) {
            e.target.action = `/admin/${this.action}/${this.type}s/${this.item}`
            e.target.submit()
        }
    }))
})