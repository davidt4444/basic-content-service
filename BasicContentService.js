class BasicContentService{
    static page_cache = '';
    admin=false;
    currentPage=0;
    data = [];
    server = "";
    constructor(data, server, admin=false)
    {
        this.admin=admin;
        this.currentPage=0;
        this.data = data;
        this.server = server;
        document.getElementById("resultXml").style.display="none";
        this.initialize();

    }

    showHideXml(){
        var x = document.getElementById("resultXml");
        if (x.style.display === "none") {
          x.style.display = "block";
        } else {
          x.style.display = "none";
        }    }
    nextPage(){
        if(this.currentPage<this.data.length-1)
        {
            this.currentPage++;
        }
        //this will change thee path to the post without reload
        //To keep it in the same page
        // this.loadContent();
        //The alternative is this. It will allow the browser back button to work. 
        var path = window.location.href.replace(window.location.search, "")+"?uniqueId="+this.data[this.currentPage].uniqueId;
        window.location.href=path;
    }
    previousPage(){
        if(this.currentPage>=1)
        {
            this.currentPage--;
        }
        //this will change thee path to the post without reload
        //To keep it in the same page
        // this.loadContent();
        //The alternative is this. It will allow the browser back button to work. 
        var path = window.location.href.replace(window.location.search, "")+"?uniqueId="+this.data[this.currentPage].uniqueId;
        window.location.href=path;
    }
    changePage(pageNum){
        if(pageNum<this.data.length && pageNum>=0)
        {
            this.currentPage=pageNum;
        }
        //this will change thee path to the post without reload
        //To keep it in the same page
        // this.loadContent();
        //The alternative is this. It will allow the browser back button to work. 
        var path = window.location.href.replace(window.location.search, "")+"?uniqueId="+this.data[this.currentPage].uniqueId;
        window.location.href=path;
    }

    deletePage(pageNum){
        if(pageNum<this.data.length && pageNum>=0)
        {
            var delId = this.data[pageNum].id;
            var guid = this.data[pageNum].uniqueId;
            $.ajax({
                url: this.server+'/post/'+delId,
                type: 'DELETE',
                success: function(result) {
                    console.log(result);
                    var path = window.location.href.replace(window.location.search, "")+"?result="+guid+" deleted";
                    window.location.href=path;
                }
            });
        }

    }
    updatePage(postId,postUniqueId,postTitle,postAuthor,postCreatedAt,postContent){
        var payload={
            id: postId,
            uniqueId: postUniqueId,
            title: postTitle,
            author: postAuthor,
            createdAt: postCreatedAt,
            content: postContent,
            category:"",
            updatedAt:"",
            likesCount:0,
            authorId:0,
            isPublished:true,
            views:true
        }
        console.log(payload);
        $.ajax({
            url: this.server+'/post/',
            type: 'PATCH',
            data: JSON.stringify(payload),
            // processData: false,
            contentType: 'application/merge-patch+json',
            success: function(result) {
                console.log(result);
                var path = window.location.href.replace(window.location.search, "")+"?result=updated";
                window.location.href=path;
            }
        });

    }
    insertPage(postId,postUniqueId,postTitle,postAuthor,postCreatedAt,postContent){
        var payload={
            id: postId,
            uniqueId: postUniqueId,
            title: postTitle,
            author: postAuthor,
            createdAt: postCreatedAt,
            content: postContent,
            category:"",
            updatedAt:"",
            likesCount:0,
            authorId:0,
            isPublished:true,
            views:true
        }
        console.log(payload);
        $.ajax({
            url: this.server+'/post/',
            type: 'POST',
            data: JSON.stringify(payload),
            // processData: false,
            contentType: 'application/merge-patch+json',
            success: function(result) {
                console.log(result);
                var path = window.location.href.replace(window.location.search, "")+"?result=created";
                window.location.href=path;
            }
        });

    }

    createPage()
    {
        var header = document.createElement("h2");
        header.appendChild(
                document.createTextNode("Editing - A new post")
                );
        document.getElementById("result_title").innerHTML="";    
        document.getElementById("result_title").appendChild(header);    
        
                    
        document.getElementById("result").innerHTML="";
        var container = document.createElement("ul");
        var holder = document.createElement("li");
        holder.setAttribute("class", "postListViewEntry");
        holder.setAttribute("id", "postListViewEntry");
        holder.appendChild(document.createTextNode("Title"));
        var input = document.createElement("input");
        input.setAttribute("id", "pageTitle");
        holder.appendChild(input);
        container.appendChild(holder);
        
        holder = document.createElement("li");
        holder.setAttribute("class", "postListViewEntry");
        holder.setAttribute("id", "postListViewEntry");
        holder.appendChild(document.createTextNode("Author"));
        input = document.createElement("input");
        input.setAttribute("id", "pageAuthor");
        holder.appendChild(input);
        container.appendChild(holder);
        
        holder = document.createElement("li");
        holder.setAttribute("class", "postListViewEntry");
        holder.setAttribute("id", "postListViewEntry");
        holder.appendChild(document.createTextNode("Content"));
        input = document.createElement("textarea");
        input.setAttribute("id", "pageContent");
        holder.appendChild(input);
        container.appendChild(holder);

        holder = document.createElement("li");
        holder.setAttribute("class", "postListViewEntry");
        holder.setAttribute("id", "postListViewEntry");
        input = document.createElement("Button");
        input.appendChild(document.createTextNode("Submit"))
        input.setAttribute("onclick", "bcs.insertPage("+
        "0,"+
        "\"00000000-0000-0000-0000-000000000000\","+
        "document.getElementById(\"pageTitle\").value,"+
        "document.getElementById(\"pageAuthor\").value,\""+
        "1-1-1772\","+
        "document.getElementById(\"pageContent\").value"+
        ")");
        
        holder.appendChild(input);
        container.appendChild(holder);

        document.getElementById("result").appendChild(container);
        // If loading from full value
        //document.getElementById("result").innerHTML=this.data[this.currentPage].content;
    }
    editPage(pageNum)
    {
        var header = document.createElement("h2");
        header.appendChild(
                document.createTextNode("Editing - "+this.data[pageNum].uniqueId)
                );
        document.getElementById("result_title").innerHTML="";    
        document.getElementById("result_title").appendChild(header);    
        
                    
        $.getJSON(this.server+'/post/'+this.data[pageNum].uniqueId, function(ret) {
            document.getElementById("result").innerHTML="";
            var container = document.createElement("ul");
            var holder = document.createElement("li");
            holder.setAttribute("class", "postListViewEntry");
            holder.setAttribute("id", "postListViewEntry");
            holder.appendChild(document.createTextNode("Title"));
            var input = document.createElement("input");
            input.setAttribute("id", "pageTitle");
            input.setAttribute("value", ret.title);
            holder.appendChild(input);
            container.appendChild(holder);
            
            holder = document.createElement("li");
            holder.setAttribute("class", "postListViewEntry");
            holder.setAttribute("id", "postListViewEntry");
            holder.appendChild(document.createTextNode("Date: "+ret.createdAt));
            container.appendChild(holder);
            
            holder = document.createElement("li");
            holder.setAttribute("class", "postListViewEntry");
            holder.setAttribute("id", "postListViewEntry");
            holder.appendChild(document.createTextNode("Author"));
            input = document.createElement("input");
            input.setAttribute("id", "pageAuthor");
            input.setAttribute("value", ret.author);
            holder.appendChild(input);
            container.appendChild(holder);
            
            holder = document.createElement("li");
            holder.setAttribute("class", "postListViewEntry");
            holder.setAttribute("id", "postListViewEntry");
            holder.appendChild(document.createTextNode("Content"));
            input = document.createElement("textarea");
            input.setAttribute("id", "pageContent");
            input.appendChild(document.createTextNode(ret.content));
            holder.appendChild(input);
            container.appendChild(holder);

            holder = document.createElement("li");
            holder.setAttribute("class", "postListViewEntry");
            holder.setAttribute("id", "postListViewEntry");
            input = document.createElement("Button");
            input.appendChild(document.createTextNode("Submit"))
            input.setAttribute("onclick", "bcs.updatePage("+
            ret.id+",\""+
            ret.uniqueId+"\","+
            "document.getElementById(\"pageTitle\").value,"+
            "document.getElementById(\"pageAuthor\").value,\""+
            ret.createdAt+"\","+
            "document.getElementById(\"pageContent\").value"+
            ")");
            holder.appendChild(input);
            container.appendChild(holder);

            document.getElementById("result").appendChild(container);
        });
        // If loading from full value
        //document.getElementById("result").innerHTML=this.data[this.currentPage].content;
    }

    loadContent()
    {
        var path = window.location.href.replace(window.location.search, "");
        if(this.data.length>0)
        {
            path += "?uniqueId="+this.data[this.currentPage].uniqueId;
            //this will change thee path to the post without reload
            // window.history.pushState("", window.title, path);
            var ahref = document.createElement("a");
            ahref.setAttribute("href",path);
            var header = document.createElement("h2");
            header.appendChild(
                    document.createTextNode(this.data[this.currentPage].title)
                    );
            ahref.appendChild(header);
            document.getElementById("result_title").innerHTML="";    
            document.getElementById("result_title").appendChild(ahref);    
            
            var holder = document.createElement("div");
            holder.setAttribute("class", "postDate");
            holder.setAttribute("id", "postDate");
            holder.appendChild(document.createTextNode("By: "+this.data[this.currentPage].author));
            document.getElementById("result_title").appendChild(holder);
            
            holder = document.createElement("div");
            holder.setAttribute("class", "postDate");
            holder.setAttribute("id", "postDate");
            holder.appendChild(document.createTextNode("Date: "+this.data[this.currentPage].createdAt));
            document.getElementById("result_title").appendChild(holder);
            
            $.getJSON(this.server+'/post/'+this.data[this.currentPage].uniqueId, function(ret) {
                var preContainer = document.createElement("xmp");
                preContainer.innerHTML=ret.content;
                document.getElementById("resultXml").innerHTML="";
                document.getElementById("resultXml").appendChild(preContainer);
                document.getElementById("result").innerHTML=ret.content;
            });
            // If loading from full value
            //document.getElementById("result").innerHTML=this.data[this.currentPage].content;
        }
    }
    getPathVariable(find)
    {
        var queryString=window.location.search;
        queryString=queryString.replace("?", "");
        var keyValue = queryString.split("&");
        for(var i=0; i<keyValue.length;i++)
        {
            var pair = keyValue[i].split("=");
            if(pair[0]===find)
            {
                return pair[1];
            }
        }
    }
    initialize()
    {
        var guid = this.getPathVariable("uniqueId");
        var unset = true;
        for(var i=0;i<this.data.length;i++)
        {
            if(this.data[i].uniqueId===guid)
            {
                this.currentPage=i;
                unset=false;
            }
        }
        if(unset && this.data.length>0)
        {
            this.currentPage=this.data.length-1;
        }
        var collection = document.createElement("ul");
        var item = document.createElement("li");
        item.setAttribute("class", "postListViewEntry")
        item.setAttribute("id", "postListViewEntry")
        var link=document.createElement("a");
        link.setAttribute("href", "https://www.thenameofyourbrand.com/index.html");
        link.appendChild(document.createTextNode("Home"));
        item.appendChild(link);
        collection.appendChild(item);
        for(i=0;i<this.data.length;i++)
        {
            item = document.createElement("li");
            item.setAttribute("class", "postListViewEntry")
            item.setAttribute("id", "postListViewEntry")
            link=document.createElement("a");
            link.setAttribute("onclick", "bcs.changePage("+i+")");
            if(i==0){
                link.appendChild(document.createTextNode("Introduction: "+this.data[i].title));
            }
            else{
                link.appendChild(document.createTextNode("Page"+(i)+": "+this.data[i].title));
            }
            item.appendChild(link);

            // var container = document.createElement("ul");
            // var holder = document.createElement("li");
            // holder.setAttribute("class", "postListViewEntry");
            // holder.setAttribute("id", "postListViewEntry");
            // holder.appendChild(document.createTextNode("By: "+this.data[i].author));
            // container.appendChild(holder);
            
            // holder = document.createElement("li");
            // holder.setAttribute("class", "postListViewEntry");
            // holder.setAttribute("id", "postListViewEntry");
            // holder.appendChild(document.createTextNode("Date: "+this.data[i].createdAt));
            // container.appendChild(holder);
            // item.appendChild(container);
            
            if(this.admin)
            {
                var submenu = document.createElement("ul");
                
                var editItem = document.createElement("li");
                editItem.setAttribute("class", "postModify")
                editItem.setAttribute("id", "postModify")
                var editLink=document.createElement("a");
                editLink.setAttribute("onclick", "bcs.editPage("+i+")");
                editLink.appendChild(document.createTextNode("Edit"));
                editItem.appendChild(editLink);
                submenu.appendChild(editItem);

                var deleteItem = document.createElement("li");
                deleteItem.setAttribute("class", "postModify")
                deleteItem.setAttribute("id", "postModify")
                var deleteLink=document.createElement("a");
                deleteLink.setAttribute("onclick", "bcs.deletePage("+i+")");
                deleteLink.appendChild(document.createTextNode("Delete"));
                deleteItem.appendChild(deleteLink);
                submenu.appendChild(deleteItem);
                
                item.appendChild(submenu);
            }
            collection.appendChild(item);
        }
        document.getElementById("postListView").appendChild(collection);
        this.loadContent();
        // JSON result in `data` variable

    }
    static getPosition(string, subString, index) {
        return string.split(subString, index).join(subString).length;
    }
    static rss(data){
        var site = "https://www.thenameofyourbrand.com/";
        var base = site+"blog.html";
        var rss_link = site+"rss.html";
        var collection = document.createElement("channel");
        var element = document.createElement("title");
        element.appendChild(document.createTextNode("The Name of Your Brand"));
        collection.appendChild(element);
        
        element = document.createElementNS("http://search.yahoo.com/mrss/", "link");
        element.appendChild(document.createTextNode(""+base));
        collection.appendChild(element);
        
        element = document.createElement("atom:link");
        element.setAttribute("href", rss_link);
        element.setAttribute("rel", "self");
        element.setAttribute("type", "application/rss+xml");
        collection.appendChild(element);
        
        element = document.createElement("description");
        element.appendChild(document.createTextNode("The blog for The Name of Your Brand"));
        collection.appendChild(element);
        
        element = document.createElement("language");
        element.appendChild(document.createTextNode("en-us"));
        collection.appendChild(element);
        var date = new Date();
        
        element = document.createElement("copyright");
        element.appendChild(document.createTextNode("Copyright "+date.getFullYear()+" Thigpen Media Group LLC"));
        collection.appendChild(element);
        
        element = document.createElement("lastBuildDate");
        element.appendChild(document.createTextNode(date.toLocaleString()));
        collection.appendChild(element);
        
        element = document.createElementNS("http://search.yahoo.com/mrss/", "pubDate");
        element.appendChild(document.createTextNode(date.toLocaleString()));
        collection.appendChild(element);
        
        for(var i=0;i<data.length;i++)
        {
            var item = document.createElement("item");
            element = document.createElementNS("http://search.yahoo.com/mrss/", "link");
            element.appendChild(document.createTextNode(base+"?uniqueId="+data[i].uniqueId));
            item.appendChild(element);
            
            element = document.createElement("atom:link");
            element.setAttribute("href", base+"?uniqueId="+data[i].uniqueId);
            element.setAttribute("rel", "standout");
            item.appendChild(element);
            
            element = document.createElement("guid");
            element.setAttribute("isPermaLink", "true");
            element.appendChild(document.createTextNode(base+"?uniqueId="+data[i].uniqueId));
            item.appendChild(element);
            
            element = document.createElement("title");
            element.appendChild(document.createTextNode(data[i].title));
            item.appendChild(element);
            
            var holder = document.createElement("div");
            holder.innerHTML = data[i].content;
            var holderInnerText = holder.innerText.substring(0,
                this.getPosition(holder.innerText, ".", 2))+"";
            
            element = document.createElement("description");
            element.appendChild(document.createTextNode(holderInnerText));
            item.appendChild(element);
            
            element = document.createElement("dc:creator");
            element.appendChild(document.createTextNode(data[i].author));
            item.appendChild(element);
            
            element = document.createElement("content:encoded");
            element.appendChild(document.createTextNode(data[i].content));
            item.appendChild(element);
            
            element = document.createElementNS("http://search.yahoo.com/mrss/", "pubDate");
            element.appendChild(document.createTextNode(data[i].createdAt));
            item.appendChild(element);
            
            collection.appendChild(item);
        }
        var rss = document.createElement("rss");
        rss.setAttribute("xmlns:dc", "http://purl.org/dc/elements/1.1/");
        rss.setAttribute("xmlns:media", "http://search.yahoo.com/mrss/");
        rss.setAttribute("xmlns:atom", "http://www.w3.org/2005/Atom");
        rss.setAttribute("xmlns:content", "http://purl.org/rss/1.0/modules/content/");
        rss.setAttribute("version", "2.0");
        rss.appendChild(collection);
        var pre = document.createElement("pre");
        // pre.appendChild(rss);
        pre.appendChild(document.createTextNode(rss.outerHTML));
        document.getElementById("feed").appendChild(pre);
        
    }
    static checkin(server){
        var insert = encodeURIComponent(window.location.href+" "+navigator.languages.toString())
        if(BasicContentService.page_cache==insert){}
        else{
            BasicContentService.page_cache=insert;
            $.ajax({
                url: server+'/'+insert,
                type: 'GET'
            });
        }
    }
}
