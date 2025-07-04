from os import path
from dataclasses import dataclass
from pathlib import Path
from .common import Z64_BaseElement, get_xml_root


@dataclass
class Z64_ParameterElement:
    type: str  # bool, enum, type, property, etc...
    index: int
    mask: int
    name: str
    subType: str  # used for <Flag> and <Collectible>
    target: str
    tiedTypes: list[int]
    items: list[tuple[int, str]]  # for <Type> and <Enum>, int is "Value"/"Params" and str is the name
    valueRange: list[int]


@dataclass
class Z64_ListElement:
    key: str
    name: str
    value: int


@dataclass
class Z64_ActorElement(Z64_BaseElement):
    category: str
    tiedObjects: list[str]
    params: list[Z64_ParameterElement]


class Z64_ActorData:
    """Everything related to OoT Actors"""

    def __init__(self, game: str):
        # Path to the ``ActorList.xml`` file
        xml_path = Path(f"{path.dirname(path.abspath(__file__))}/xml/{game.lower()}_actor_list.xml")
        actor_root = get_xml_root(xml_path.resolve())

        # general actor list
        self.actorList: list[Z64_ActorElement] = []

        # list elements
        self.chestItems: list[Z64_ListElement] = []
        self.collectibleItems: list[Z64_ListElement] = []
        self.messageItems: list[Z64_ListElement] = []

        listNameToList = {
            "Chest Content": self.chestItems,
            "Collectibles": self.collectibleItems,
            "Elf_Msg Message ID": self.messageItems,
        }

        for elem in actor_root.iterfind("List"):
            listName = elem.get("Name")
            if listName is not None:
                for item in elem:
                    listNameToList[listName].append(
                        Z64_ListElement(item.get("Key"), item.get("Name"), int(item.get("Value"), base=16))
                    )

        for actor in actor_root.iterfind("Actor"):
            tiedObjects = []
            objKey = actor.get("ObjectKey")
            actorName = f"{actor.attrib['Name']} - {actor.attrib['ID'].removeprefix('ACTOR_')}"

            if objKey is not None:  # actors don't always use an object
                tiedObjects = objKey.split(",")

            # parameters
            params: list[Z64_ParameterElement] = []
            for elem in actor:
                elemType = elem.tag
                if elemType != "Notes":
                    items: list[tuple[int, str]] = []
                    if elemType == "Type" or elemType == "Enum":
                        for item in elem:
                            key = "Params" if elemType == "Type" else "Value"
                            name = item.text.strip() if elemType == "Type" else item.get("Name")
                            if key is not None and name is not None:
                                items.append((int(item.get(key), base=16), name))

                    # not every actor have parameters tied to a specific actor type
                    tiedTypes = elem.get("TiedActorTypes")
                    tiedTypeList = []
                    if tiedTypes is not None:
                        tiedTypeList = [int(val, base=16) for val in tiedTypes.split(",")]

                    defaultName = f"{elem.get('Type')} {elemType}"
                    valueRange = elem.get("ValueRange")
                    params.append(
                        Z64_ParameterElement(
                            elemType,
                            int(elem.get("Index", "1")),
                            int(elem.get("Mask", "0xFFFF"), base=16),
                            elem.get("Name", defaultName if not "None" in defaultName else elemType),
                            elem.get("Type"),
                            elem.get("Target", "Params"),
                            tiedTypeList,
                            items,
                            [int(val) for val in valueRange.split("-")] if valueRange is not None else [None, None],
                        )
                    )

            self.actorList.append(
                Z64_ActorElement(
                    actor.attrib["ID"],
                    actor.attrib["Key"],
                    actorName,
                    int(actor.attrib["Index"]),
                    actor.attrib["Category"],
                    tiedObjects,
                    params,
                )
            )

        self.actorsByKey = {actor.key: actor for actor in self.actorList}
        self.actorsByID = {actor.id: actor for actor in self.actorList}

        self.chestItemByKey = {elem.key: elem for elem in self.chestItems}
        self.collectibleItemsByKey = {elem.key: elem for elem in self.collectibleItems}
        self.messageItemsByKey = {elem.key: elem for elem in self.messageItems}

        self.chestItemByValue = {elem.value: elem for elem in self.chestItems}
        self.collectibleItemsByValue = {elem.value: elem for elem in self.collectibleItems}
        self.messageItemsByValue = {elem.value: elem for elem in self.messageItems}

        # list of tuples used by Blender's enum properties

        lastIndex = max(1, *(actor.index for actor in self.actorList))
        self.ootEnumActorID = [("None", f"{i} (Deleted from the XML)", "None") for i in range(lastIndex)]
        self.ootEnumActorID.insert(0, ("Custom", "Custom Actor", "Custom"))

        doorTotal = 0
        for actor in self.actorList:
            if actor.category == "ACTORCAT_DOOR":
                doorTotal += 1
        self.ootEnumTransitionActorID = [("None", f"{i} (Deleted from the XML)", "None") for i in range(doorTotal)]
        self.ootEnumTransitionActorID.insert(0, ("Custom", "Custom Actor", "Custom"))

        i = 1
        for actor in self.actorList:
            self.ootEnumActorID[actor.index] = (actor.id, actor.name, actor.id)
            if actor.category == "ACTORCAT_DOOR":
                self.ootEnumTransitionActorID[i] = (actor.id, actor.name, actor.id)
                i += 1

        self.ootEnumChestContent = [(elem.key, elem.name, elem.key) for elem in self.chestItems]
        self.ootEnumCollectibleItems = [(elem.key, elem.name, elem.key) for elem in self.collectibleItems]
        self.ootEnumNaviMessageData = [(elem.key, elem.name, elem.key) for elem in self.messageItems]

        self.ootEnumChestContent.insert(0, ("Custom", "Custom Value", "Custom"))
        self.ootEnumCollectibleItems.insert(0, ("Custom", "Custom Value", "Custom"))
        self.ootEnumNaviMessageData.insert(0, ("Custom", "Custom Value", "Custom"))

    def getItems(self, actorUser: str):
        if actorUser == "Actor":
            return self.ootEnumActorID
        elif actorUser == "Transition Actor":
            return self.ootEnumTransitionActorID
        elif actorUser == "Entrance":
            return [(self.actorsByKey["player"].id, self.actorsByKey["player"].name, self.actorsByKey["player"].id)]
        else:
            raise ValueError("ERROR: The Actor User is unknown!")
