document.addEventListener('alpine:init', () => {
    Alpine.data('modal', () => ({
        visible: false,
        message: null,
        next: null,
        sending: false,
        open(e) {
            this.sending = false
            this.message = e.target.dataset.message
            this.next = e.target.dataset.next
            this.visible = true
        },
        close() {
            if (this.sending) return
            this.visible = false
            this.message = null
            this.next = null
        },
        submit(e) {
            this.sending = true
            e.target.action = this.next
            e.target.submit()
        }
    }))
})