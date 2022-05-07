<script>
    import { useNavigate } from "svelte-navigator";

    const navigate = useNavigate();

/*
    async function fetchAnalytics() {
        const response = await fetch('http://172.26.134.62/api/analytics')
        return await response.json()
    }
*/
</script>

<div class="container">
<!--
    {#await fetchAnalytics()}
        <p>Loading...</p>
    {:then analytics}
        {#each Object.entries(analytics) as [name, desc]}
            {name}
            <button class="button" on:click={()=>navigate({name})}>{name}</button>
            <p>{desc.description}</p>
        {/each}
    {:catch error}
        <p>{error.message}</p>
    {/await}&ndash;&gt;
-->
    <div class="relative flex items-center justify-center flex-col h-full w-full p-2 bg-white bg-opacity-30 rounded-2xl backdrop-filter">
        <span class="relative flex items-center justify-center text-2xl mb-10">Liveability in Melbourne</span>
        <p>Exploring liveability in Melbourne through the Australian Federal election 2022</p>
        <p></p>
        <p>Select a livability indicator</p>
        <span class="btn-group justify-center items-center">
        <button class="button" on:click={()=>navigate('opportunity')}>Opportunity</button>
        <button class="button" on:click={()=>navigate('social-engagement')}>Social Engagement</button>
    </span>
    </div>
</div>


<style>
    .container {
        @apply h-full w-11/12 absolute right-0 top-0 z-10;
    }

    h1 {

    }

    .button {
        @apply bg-white border-2 border-blue-300 rounded-2xl p-2 hover:bg-blue-300 hover:text-white hover:border-white;
    }

    .btn-group {
        @apply relative flex items-center justify-center space-x-4 w-1/2;
        text-align: center;
    }

    p {
        text-align: center;
        margin: 5px;
    }
</style>