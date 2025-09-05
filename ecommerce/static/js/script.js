
          function toggleDropdown() {
            const menu = document.getElementById('dropdown-menu');
            menu.classList.toggle('hidden');
          }

  // Close dropdown when clicking outside
  document.addEventListener('click', function(event) {
    const dropdown = document.getElementById('dropdown-container');
    if (!dropdown.contains(event.target)) {
      document.getElementById('dropdown-menu').classList.add('hidden');
    }
  });

