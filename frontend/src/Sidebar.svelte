<script>
    import Tailwindcss from './Tailwindcss.svelte';
    import SidebarIcon from './SidebarIcon.svelte';
    import { useNavigate } from "svelte-navigator";

    const navigate = useNavigate();
</script>

<Tailwindcss/>
<main class="fixed top-0 left-0 h-screen w-1/12 m-0 flex flex-col bg-gray-600 text-white shadow-lg z-30">
    <div class="fa-solid fa-bullhorn icon group">
        <span class="tooltip hidden group-hover:block">Social Engagement</span>
    </div>
    <div class="fa-solid fa-scale-unbalanced icon group">
        <span class="tooltip hidden group-hover:block">Opportunity</span>
    </div>
    <div class="fa-solid fa-user-group icon group">
        <span class="tooltip hidden group-hover:block">Diversity Map</span>
    </div>
    <div class="fa-solid fa-person-booth icon group">
        <span class="tooltip hidden group-hover:block">Election Issues</span>
    </div>
    <div class="fa-solid fa-square-check icon group">
        <span class="tooltip hidden group-hover:block">Scott Morrison Approval Ratings</span>
    </div>
</main>

<style>
    .icon {
        font-size: 3.5em;
        margin: 1rem;
        @apply relative flex items-center justify-center h-12 w-12 mb-10 p-10 mx-auto shadow-lg
        bg-gray-800 text-green-500 hover:bg-green-600 hover:text-white rounded-3xl transition-all duration-200 ease-linear cursor-pointer;
    }
    .tooltip {
        @apply absolute w-auto p-2 m-2 min-w-max left-20 rounded-md shadow-md text-white bg-gray-900 text-xs font-bold transition-all duration-100 scale-0 origin-left;
    }

</style>