var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
  return new bootstrap.Tooltip(tooltipTriggerEl)
})





// show password


// log-out notification

function logoutNotify(){
  Swal.fire({
    title: 'Log-out now?',
    text: "Do you want to logout now?",
    icon: 'question',
    showCancelButton: true,
    confirmButtonColor: '#3085d6',
    cancelButtonColor: '#d33',
    confirmButtonText: 'Log-out'
  }).then((result) => {
    if (result.isConfirmed) {
      window.location.href = '/accounts/logout/'
    }
  })
}