<script>

let nodeRef;

</script>

<div class="relative flex items-center justify-center flex-col h-full w-full p-2 bg-white bg-opacity-30 rounded-2xl backdrop-filter backdrop-blur-sm border-4 border-blue-800 z-40" bind:this={nodeRef} >
    <span class="relative flex items-center justify-center text-2xl mb-10">Welcome to Website</span>
    <span class="btn-group">
      <span class="button" on:click={() => nodeRef.parentNode.removeChild(nodeRef)}>
        Remove me :( and add data :)
    </span>
    <span class="button" on:click={() => nodeRef.parentNode.removeChild(nodeRef)}>
      Remove me :( and add different data :)
  </span>
    </span>
</div>

<style>
  .btn-group {
    @apply relative flex items-center justify-center space-x-4 w-1/2;
  }
  .button {
    @apply bg-white border-2 border-blue-300 rounded-2xl p-2 hover:bg-blue-300 hover:text-white hover:border-white;
  }
</style>